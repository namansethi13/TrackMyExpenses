import CommonTable from "../common-table/CommonTable";
import type { CommonTableProps } from "../common-table/CommonTable";

export default function RecentExpensesTable({tableData} : CommonTableProps) {
    return (
        <CommonTable tableData={tableData} />
    );
}
