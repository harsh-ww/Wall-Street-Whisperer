import React from "react";
import { Table, Thead, Tbody, Tr, Th, Td, chakra } from "@chakra-ui/react";
import { TriangleDownIcon, TriangleUpIcon } from "@chakra-ui/icons";
import {
  useReactTable,
  flexRender,
  getCoreRowModel,
  ColumnDef,
  SortingState,
  getSortedRowModel,
} from "@tanstack/react-table";

export type DataGridProps<Data extends object> = {
  data: Data[]; // Array of data to be displayed in the grid
  columns: ColumnDef<Data, any>[]; // Configuration for the columns of the grid
};

export function DataGrid<Data extends object>({
  data,
  columns,
}: DataGridProps<Data>) {
  // State for managing sorting
  const [sorting, setSorting] = React.useState<SortingState>([]);
  // Initialize the table instance using useReactTable hook
  const table = useReactTable({
    columns,
    data,
    getCoreRowModel: getCoreRowModel(),
    onSortingChange: setSorting,
    getSortedRowModel: getSortedRowModel(),
    state: {
      sorting,
    },
  });

  return (
    <Table>
      <Thead>
        {table.getHeaderGroups().map((headerGroup) => (
          <Tr key={headerGroup.id}>
            {headerGroup.headers.map((header) => {
              // Extract metadata from column definition
              const meta: any = header.column.columnDef.meta;
              return (
                <Th
                  key={header.id}
                  onClick={header.column.getToggleSortingHandler()} // Handle sorting when header cell is clicked
                  isNumeric={meta?.isNumeric} // Set cell alignment based on metadata
                >
                  {flexRender(
                    header.column.columnDef.header,
                    header.getContext()
                  )}

                  {/* Render sorting icons */}
                  <chakra.span pl="4">
                    {header.column.getIsSorted() ? (
                      header.column.getIsSorted() === "desc" ? ( // If sorted in descending order
                        <TriangleDownIcon aria-label="sorted descending" />
                      ) : (
                        <TriangleUpIcon aria-label="sorted ascending" />
                      )
                    ) : null}
                  </chakra.span>
                </Th>
              );
            })}
          </Tr>
        ))}
      </Thead>
      <Tbody>
        {table.getRowModel().rows.map((row) => (
          <Tr key={row.id}>
            {/* Render cells within each row */}
            {row.getVisibleCells().map((cell) => {
              const meta: any = cell.column.columnDef.meta;
              return (
                <Td key={cell.id} isNumeric={meta?.isNumeric}>
                  {/* Render cell content */}
                  {flexRender(cell.column.columnDef.cell, cell.getContext())}
                </Td>
              );
            })}
          </Tr>
        ))}
      </Tbody>
    </Table>
  );
}
