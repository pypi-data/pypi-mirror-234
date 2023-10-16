from typing import List, Tuple
import pandas as pd
from dataprojects.validation import Validation
import re


class WallMartTemplate:
    def __init__(self, fixtures, rowdf, obj) -> None:
        self.fixtures = fixtures
        self.rowdf = rowdf
        self.obj = obj

    def get_filterd_and_errors(self, validation1, errortypes) -> List[List[str]]:
        sorting = Validation(self.rowdf, validation1, errortypes=errortypes)
        data = sorting.get_formetted_data()
        errors = []
        maindf = []
        if self.fixtures is not None:
            for i in self.fixtures:
                if sorting.validate_po_wise_transections(
                    data, i["PoNo"], validationlength=i["validationlength"]
                ):
                    maindf.append(i)
                else:
                    errors.append(i)
        return [maindf, errors]

    def get_filterd_and_errors_invoices(self, maindf, errors) -> List[pd.DataFrame]:
        df_list2 = []
        for fd in maindf:
            rslt_df = self.rowdf[
                self.rowdf["PURCHASE ORDER NO"].str.contains(fd["PoNo"])
            ]
            df_list2.append(rslt_df)
        df_list = []
        for fd in errors:
            rslt_df = self.rowdf[
                self.rowdf["PURCHASE ORDER NO"].str.contains(fd["PoNo"])
            ]
            df_list.append(rslt_df)
        return [pd.concat(df_list), pd.concat(df_list2)]

    def get_finalmisingdata_and_finaldata_df(
        self, validation1, errortypes, maindf, newdf
    ) -> pd.DataFrame:
        sorteddata = Validation(newdf, validation1, errortypes=errortypes)
        maindf = pd.concat(
            [pd.DataFrame.from_records(sorteddata.get_sorted_data()[0]), maindf]
        )
        newdf = pd.DataFrame.from_records(sorteddata.get_sorted_data()[1])
        maindf = Validation(maindf, validation1, errortypes=errortypes)
        maindf = pd.DataFrame.from_records(maindf.get_sorted_data()[0])
        missingdatadf = []
        maindfdata = []
        for jh in self.fixtures:
            if sorteddata.validate_po_wise_transections(
                maindf, jh["PoNo"], validationlength=jh["validationlength"]
            ):
                rslt_df = maindf[maindf["PURCHASE ORDER NO"].str.contains(jh["PoNo"])]
                maindfdata.append(rslt_df)
            else:
                rslt_df = maindf[maindf["PURCHASE ORDER NO"].str.contains(jh["PoNo"])]
                existingdata = [int(x) for x in rslt_df["Sr.No"].to_list()]
                missing = [x + 1 for x in range(jh["validationlength"])]
                finalmissingdata = []
                for x in missing:
                    if x not in existingdata:
                        finalmissingdata.append(x)
                missingdatadf.append([rslt_df, finalmissingdata])
        missingdata = sorteddata.fillmissingdata(self.obj, missingdatadf, self.fixtures)
        missingdf = [pd.DataFrame.from_records(x) for x in list(missingdata)]
        finaldf = []
        for x in missingdatadf:
            for y in missingdf:
                srno = [int(r) for r in y["Sr.No"].to_list()]
                s = x[0]["PURCHASE ORDER NO"].to_list()
                sx = y["PURCHASE ORDER NO"].to_list()
                if s != []:
                    if s[0] in sx:
                        finaldfd = pd.concat([x[0], y])
                        finaldf.append(finaldfd)
        finalmissingdata = pd.concat(finaldf)
        return pd.concat([finalmissingdata, maindf]), sorteddata

    def filter_and_format_taxdetails(self, finaldaat) -> pd.DataFrame:
        totallist = []
        for uyte, jhcfsdj in finaldaat.iterrows():
            total = jhcfsdj["Tax Details"].split("-")[-1]
            total = total.replace("0.00", "")
            try:
                total = float(total)
            except ValueError as E:
                linecost = jhcfsdj["Line Cost Excl Tax"]
                if "IN" in jhcfsdj["Line Cost Excl Tax"]:
                    linecost = jhcfsdj["Line Cost Excl Tax"].split("IN")[0][
                        0 : int(
                            round(len(jhcfsdj["Line Cost Excl Tax"].split("IN")[0]) / 2)
                        )
                        - 1
                    ]
                if "IN" in jhcfsdj["Tax Details"].split("-")[1]:
                    total = float(linecost) + float(
                        jhcfsdj["Tax Details"].split("-")[1].replace("IN", "")
                    )
                else:
                    total = float(linecost) + float(
                        jhcfsdj["Tax Details"].split("-")[1]
                    )
                jhcfsdj["Line Cost Excl Tax"] = " ".join([linecost, " "])
                jhcfsdj["Cost"] = linecost
                if len(jhcfsdj["Tax Details"]) < len(
                    "IN:  IGST(12%) - 342.39 - IN: GST Comp. CESS(0.00%) - 0.00"
                ):
                    data = jhcfsdj["Tax Details"]
                    jhcfsdj[
                        "Tax Details"
                    ] = f"IN:  {data[:-2]} - IN: GST Comp. CESS(0.00%) - 0.00"
            linecostex = jhcfsdj["Line Cost Excl Tax"].split(" ")[0]
            texdetails = jhcfsdj["Tax Details"].split("-")[0] + "- 0.00"
            if len(texdetails) < 32:
                texdetails = jhcfsdj["Tax Details"]
            else:
                rowtax = " ".join(jhcfsdj["Line Cost Excl Tax"].split(" ")[1:])
                texdetails = "{} - {}".format(rowtax, texdetails)
            jhcfsdj["Line Cost Excl Tax"] = float(linecostex)
            jhcfsdj["Total Amount incl tax"] = float(total)
            jhcfsdj["Tax Details"] = texdetails
            totallist.append(jhcfsdj.to_dict())
        return pd.DataFrame.from_records(totallist)

    def drop_duplicates_with_dynamic_subsets(
        self, rowdataframe, subsets
    ) -> pd.DataFrame:
        return rowdataframe.drop_duplicates(subset=subsets)

    def validating_and_applying_changes(
        self, fixtures, sorteddata, df
    ) -> Tuple[pd.DataFrame, List[str]]:
        dfew = []
        pos = []
        for jh in fixtures:
            if sorteddata.validate_po_wise_transections(
                df, jh["PoNo"], validationlength=jh["validationlength"]
            ):
                rslt_df = df[df["PURCHASE ORDER NO"].str.contains(jh["PoNo"])]
                costwithoutax = rslt_df["Line Cost Excl Tax"].sum()
                costwithtax = rslt_df["Total Amount incl tax"].sum()
                totalgfd = []
                for k, v in rslt_df.iterrows():
                    v["Total Cost Without Tax"] = costwithoutax
                    v["Grand Total Amount incl tax"] = costwithtax
                    v["Total tax Amount"] = costwithtax - costwithoutax
                    v["Vendor Stock"] = ""
                    v["ORDER DATE"] = "".join(v["ORDER DATE"].split(":"))
                    v["PO CANCEL DATE"] = "".join(v["PO CANCEL DATE"].split(":"))
                    totalgfd.append(v.to_dict())
                dfew.append(pd.DataFrame.from_records(totalgfd))
            else:
                pos.append(jh["PoNo"])
        return [pd.concat(dfew), pos]

    def get_selected_data(self, validation1, errortypes, subset, dfs=[]):
        valobj = []
        for i in range(len(dfs)):
            valobj.append(Validation(dfs[i], validation1, errortypes=errortypes))
        alldfs = []
        for x in valobj:
            for j in x.get_sorted_data():
                if j != []:
                    alldfs.append(j)
        alldfsq = []
        for ds, hg in enumerate(alldfs):
            if ds == 0:
                alldfsq = hg
            else:
                alldfsq += hg

        rowdfs = pd.DataFrame.from_records(alldfsq)
        validate = Validation(rowdfs, validation1, errortypes=errortypes)
        validateq = validate.get_formetted_data()
        return validateq

    def formet_single_data(self, data, validation1, errortypes, validatorcallback=None):
        validation = Validation(
            pd.DataFrame.from_records([data]), validation1, errortypes=errortypes
        )
        df = validation.get_error_types(pd.DataFrame.from_records([data]))
        validateerrortypes = None
        formetteddata = []
        if df != []:
            for i in df:
                if type(i) == dict:
                    validateerrortypes = validation.get_identified_data(i)
                    formetteddata.append(validateerrortypes)
                else:
                    for x in i:
                        validateerrortypes = validation.get_identified_data(x)
                        formetteddata.append(validateerrortypes)
        else:
            raise ValueError("errortype not defiened", data)
        if validatorcallback is not None:
            return self.formet_single_data(
                self, data, validation1, errortypes, validatorcallback=validatorcallback
            )
        else:
            return formetteddata
