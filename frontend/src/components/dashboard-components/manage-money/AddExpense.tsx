import AddGeneric from "../generics/AddGeneric";

export default function AddExpense() {
    const handleSubmit = (event:any) => {
        console.log(event)
    }
    return (
        <AddGeneric
        title="Add Expense"
        buttonTxt="Add"
        categories = {[
            { id: 1, name: "Grocery" },
            { id: 2, name: "Electronics" },
            { id: 3, name: "Clothing" },
            { id: 4, name: "Books" },
            { id: 5, name: "Home & Kitchen" },
            { id: 6, name: "Health & Beauty" },
            { id: 7, name: "Sports & Outdoors" },
            { id: 8, name: "Toys & Games" },
            { id: 9, name: "Automotive" },
            { id: 10, name: "Pet Supplies" }
        ]}
        onFormSubmit={handleSubmit}
        />
    );
}