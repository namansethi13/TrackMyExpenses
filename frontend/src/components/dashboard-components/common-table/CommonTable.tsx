

interface TableData {
  header: string[];
  rows: string[][];
}

interface TableWithDropdown {
  rowsDropdown: true;
  tableData: TableData & { subrows: string[][][] }; 
}

interface TableWithoutDropdown {
  rowsDropdown?: false | undefined;
  tableData: TableData; 
}

export type CommonTableProps = TableWithDropdown | TableWithoutDropdown;


export default function CommonTable({ tableData }: CommonTableProps) {
    return (
        <table className="min-w-full bg-white border border-gray-200">
            <thead>
                <tr>
                    {tableData.header.map((head, idx) => (
                        <th key={idx} className="p-2 border-b border-gray-200">{head}</th>
                    ))}
                </tr>
            </thead>
            <tbody>
                {tableData.rows.map((row, rowIdx) => (
                    <tr key={rowIdx}>
                        {row.map((col, colIdx) => (
                            <td key={colIdx} className="p-2 border-b border-gray-200">
                                <span>{col}</span>

                                
                            </td>
                        ))}
                        {/* {'subrows' in tableData && tableData.subrows && tableData.subrows[rowIdx] ? (
                            <td className="p-2 border-b border-gray-200">
                                <div className="dropdown">
                                    <button className="dropdown-toggle">Toggle</button>
                                    <div className="dropdown-menu">
                                        {tableData.subrows[rowIdx].map((subrow: string[], subrowIdx: number) => (
                                            <div key={subrowIdx} className="dropdown-item">{subrow.join(", ")}</div>
                                        ))}
                                    </div>
                                </div>
                            </td>
                        ) : null} */}

                    </tr>
                ))}
            </tbody>
        </table>
    );
}