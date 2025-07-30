import {useRef, useState } from "react";

interface Category{
    id: number;
    name:string;
}

interface Props {
    title: string;
    categories: Category[];
    buttonTxt: string;
    onFormSubmit: (event: any) => void;
}

export default function AddGeneric(
    {
        title,
        categories,
        buttonTxt,
        onFormSubmit
    } : Props
) {
    const [value, setValue] = useState("")
    const inputElement = useRef(null);
    const forceNumber = (event: React.ChangeEvent<HTMLInputElement>) => {
    const inputVal = event.target.value;
    if (/^\d*$/.test(inputVal)) {
      setValue(inputVal);
    }
  };
    return (
        <main className="p-4 md:p-12 flex-1 w-full h-full items-center justify-center">
            <h1 className="text-3xl font-bold mb-6">{title}</h1>
            <form className="flex flex-col space-y-4 max-w-sm" onSubmit={(event) => {event.preventDefault(); onFormSubmit(event)}}>
                <input
                    type="text"
                    placeholder="Amount"
                    onChange={forceNumber}
                    ref={inputElement}
                    value={value}
                    className="bg-gray-100 px-4 py-3 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                />

                <select
                    name="categories"
                    id="categories"
                    className="bg-gray-100 px-4 py-3 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                >
                    {categories.map( cat => <option value={cat.id} key={cat.id}>{cat.name}</option> )}
                </select>

                <input
                    type="date"
                    name="expense-date"
                    id="expense-date"
                    className="bg-gray-100 px-4 py-3 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                />
                 <button
                        type="button"
                        className="bg-blue-400 text-white px-6 py-2 rounded-full hover:bg-blue-400 transition"
                    >
                        Today
                </button>

                <textarea
                    name="description"
                    id="description"
                    cols={20}
                    rows={4}
                    placeholder="Description"
                    className="bg-gray-100 px-4 py-3 rounded-md resize-none focus:outline-none focus:ring-2 focus:ring-blue-500"
                ></textarea>

                <div className="flex justify-center">
                    <button
                        type="submit"
                        className="bg-blue-500 text-white px-6 py-2 rounded-full hover:bg-blue-600 transition"
                    >
                       {buttonTxt}
                    </button>
                </div>
            </form>
        </main>
    );
}