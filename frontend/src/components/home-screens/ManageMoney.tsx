import { AddExpense, AddIncome } from "../dashboard-components/manage-money"
export default function ManageMoney(){
    return(
        <section
        className="flex flex-col md:flex-row">
            <AddExpense/>
            <AddIncome/>
        </section>
    )
}