import { useState } from "react";

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

export default function CommonTable({ tableData, rowsDropdown }: CommonTableProps) {
    console.log(rowsDropdown)
  const [openRows, setOpenRows] = useState<Record<number, boolean>>({});

  const toggleRow = (idx: number) => {
    setOpenRows(prev => ({ ...prev, [idx]: !prev[idx] }));
  };

  return (
    <table className="min-w-full bg-white border border-gray-200  transition-all">
      <thead>
        <tr>
          {rowsDropdown && <th className="w-10"></th>}
          {tableData.header.map((head, idx) => (
            <th key={idx} className="p-2 border-b border-gray-200 text-left">
              {head}
            </th>
          ))}
        </tr>
      </thead>
      <tbody>
        {tableData.rows.map((row, rowIdx) => (
          <Fragment key={rowIdx}>
            <tr className="align-top">
              {rowsDropdown && (
                <td className="p-2 border-b border-gray-200 text-center">
                  {tableData.subrows?.[rowIdx] ? (
                    <button
                      onClick={() => toggleRow(rowIdx)}
                      className="text-xs px-2 py-1 bg-gray-100 hover:bg-gray-200 border border-gray-300 rounded"
                    >
                      {openRows[rowIdx] ? "−" : "+"}
                    </button>
                  ) : null}
                </td>
              )}
              {row.map((col, colIdx) => (
                <td key={colIdx} className="p-2 border-b border-gray-200">
                  {col}
                </td>
              ))}
            </tr>

            {rowsDropdown && openRows[rowIdx] && (
              <tr className="bg-gray-50">
                <td colSpan={(rowsDropdown ? 1 : 0) + tableData.header.length} className="p-2 border-b border-gray-200">
                  <div className="flex flex-col gap-1 text-sm text-gray-700">
                    {tableData.subrows?.[rowIdx]?.map((subRowCells, idx) => (
                      <div key={idx} className="flex gap-8">
                        {subRowCells.map((cell, cellIdx) => (
                          <span key={cellIdx}>{cell}</span>
                        ))}
                      </div>
                    ))}
                  </div>
                </td>
              </tr>
            )}
          </Fragment>
        ))}
      </tbody>
    </table>
  );
}

import { Fragment } from "react";
