import { useEffect, useState } from "react";
import { API_URL } from "../config";
import { DataGrid } from "./DataGrid";
import { createColumnHelper } from "@tanstack/react-table";
import { Badge } from "@chakra-ui/react";
import { NavLink } from "react-router-dom";

type UnitConversion = {
    Symbol: string;
    Company: string;
    LastPrice: string;
    Change: string;
    PercentChg: string;
};

interface TrackedData {
    id: number;
    name: string;
    TickerCode: string;
    exchange: string;
    CommonName: string;
    currency: string;
    stock: {
        "open": string,
        "high": string,
        "low": string,
        "price": string,
        "volume": string,
        "latest trading day": string,
        "previous close": string,
        "change": string,
        "change percent": string
    }
}

export default function DataTable() {

    const [trackedData, setTrackedData] = useState<UnitConversion[]>([]);
    const [isLoaded, setIsLoaded] = useState(false);

    useEffect(() => {
        const fetchData = async () => {
            const res = await fetch(`${API_URL}/tracked?data=True`);
            if (!res.ok) {
                console.error("err")
                throw new Error()
            }

            const data: TrackedData[] = await res.json();

            let convertedData: UnitConversion[] = []
            const sign = (x: string) => x.startsWith("-") ? "" : "+";

            for (const company of data) {
                convertedData.push({
                    'Symbol': company.TickerCode,
                    'Company': company.name,
                    'PercentChg': company.stock["change percent"],
                    'LastPrice': `${company.currency} ${company.stock.price}`,
                    'Change': `${company.currency} ${sign(company.stock.change)}${company.stock.change}`
                })
            }

            setTrackedData(convertedData);
            setIsLoaded(true);
        }

        fetchData();
    }, [])

    const columnHelper = createColumnHelper<UnitConversion>();

    const columns = [
        columnHelper.accessor("Symbol", {
            cell: (info) => (
                <NavLink to={`/company/${info.getValue()}`}>
                    <Badge 
                        fontSize="0.9em" 
                        bg="cyan.100" 
                        _hover={{ 
                            bg: "cyan.400", 
                            transform: "translateY(-3px)",
                            transitionTimingFunction: "ease-in-out" 
                        }} 
                    >
                        {info.getValue()}
                    </Badge>
                </NavLink>
            ),
            header: "Symbol",
        }),
        columnHelper.accessor("Company", {
            cell: (info) => info.getValue(),
            header: "Company",
        }),
        columnHelper.accessor("LastPrice", {
            cell: (info) => info.getValue(),
            header: "Last Price",
        }),
        columnHelper.accessor("Change", {
            cell: (info) => info.getValue(),
            header: "Change",
        }),
        columnHelper.accessor("PercentChg", {
            cell: (info) => (
                <Badge
                    fontSize="0.9em"
                    bg={parseFloat(info.getValue().replace("%", "")) >= 0 ? "green.200" : "red.200"}
                >
                    {info.getValue()}
                </Badge>
            ),
            header: "Change%",
            meta: {
                isNumeric: true,
            },
        }),
    ];



    return (
        <DataGrid data={trackedData} columns={columns}></DataGrid>
    )
}