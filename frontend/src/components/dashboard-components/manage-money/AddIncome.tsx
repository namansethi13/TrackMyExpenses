import AddGeneric from "../generics/AddGeneric";

export default function AddIncome() {
    const handleSubmit = (event:any) => {
        console.log(event)
    }
    return (
        <AddGeneric
        title="Add Income"
        buttonTxt="Add"
        categories = {[
            { id: 1, name: "Salary" },
            { id: 2, name: "Freelance" },
            { id: 3, name: "Business Profit" },
            { id: 4, name: "Investment Returns" },
            { id: 5, name: "Interest Income" },
            { id: 6, name: "Rental Income" },
            { id: 7, name: "Dividends" },
            { id: 8, name: "Capital Gains" },
            { id: 9, name: "Royalties" },
            { id: 10, name: "Grants & Scholarships" }
        ]}
        onFormSubmit={handleSubmit}
        />
    );
}