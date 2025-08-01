import CommonTable from "../common-table/CommonTable";
import type { CommonTableProps } from "../common-table/CommonTable";

export default function ExpenseSummaryTable({tableData, rowsDropdown}: CommonTableProps) {
   return (
        rowsDropdown ? <CommonTable tableData={tableData} rowsDropdown={rowsDropdown}/> : <CommonTable tableData={tableData} />
    );
}