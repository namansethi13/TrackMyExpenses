import RecentExpenseTable from "../dashboard-components/recent-expenses-table/RecentExpensesTable";
import ExpenseSummaryDatePicker from "../dashboard-components/expense-summary-date-picker/ExpenseSummaryDatePicker";
import ExpenseSummaryTable from "../dashboard-components/expense-summary-table/ExpenseSummaryTable";
export default function Dashboard(){
    return (
        <main className="p-4 flex-1 w-full h-full md:mt-12">
            <h1 className="text-3xl font-bold text-center md:text-left">Dashboard</h1>

            <div className="mt-24">
                <h3 className="text-lg font-bold md:text-left">Recent Expenses</h3>
                <RecentExpenseTable tableData={{
                    header: ["Date", "Description", "Amount"],
                    rows: [
                        ["June 6th", "Groceries", "$50"],
                        ["June 6th", "Utilities", "$100"],
                        ["June 6th", "Rent", "$1200"],
                        ["June 7th", "Groceries", "$50"],
                        ["June 7th", "Utilities", "$100"],
                        ["June 7th", "Rent", "$1200"],
                        ["June 8th", "Groceries", "$50"],
                        ["June 8th", "Utilities", "$100"],
                        ["June 9th", "Rent", "$1200"],
                        ["June 9th", "Groceries", "$50"],
                    ]
                }} />
                
                <h3 className="text-lg font-bold md:text-left mt-12">Expense Summary</h3>
                <ExpenseSummaryDatePicker />
                <button className="mt-4 p-2 bg-blue-500 text-white rounded-lg cursor-pointer hover:bg-blue-600 transition">Generate Report</button>
                <ExpenseSummaryTable
                    rowsDropdown={true}
                    tableData={{
                        header: ["Category", "Amount"],
                        rows: [
                        ["Groceries", "$100"],
                        ["Rent", "$500"],
                        ["Utilities", "$200"]
                        ],
                        subrows: [
                        [ ["June 1", "$50"], ["June 5", "$50"] ],
                        [ ["Paid on June 3", "$500"] ],
                        [ ["Electricity", "$150"], ["Water", "$50"] ]
                        ]
                    }}/>
                        <h3 className="text-lg font-bold md:text-left mt-12">Ai Suggestions</h3>
                <div className="mt-4 p-4 bg-gray-100 rounded-lg">
                    <p className="text-gray-700">No suggestions available at the moment.</p>
                </div>

            </div>
        </main>
    )
}