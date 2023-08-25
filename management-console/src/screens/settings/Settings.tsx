import Table from '@mui/material/Table';
import TableBody from '@mui/material/TableBody';
import TableCell from '@mui/material/TableCell';
import TableContainer from '@mui/material/TableContainer';
import TableHead from '@mui/material/TableHead';
import TableRow from '@mui/material/TableRow';
import Paper from '@mui/material/Paper';
import TextField from '@mui/material/TextField';
import Autocomplete from '@mui/material/Autocomplete';

import { useGetConfigs } from "../../api/configs";
import { useCallback, useState } from 'react';
import { useDebounce } from '../../customHooks/useDebounce';

export const Settings = () => {
    const [filter, setFilter] = useState("");
    const { data: configs = {} } = useGetConfigs();
    console.log(configs)

    const onFilterChange = useCallback((value: string) => {
        setFilter(value.toLowerCase())
    }, [])
    const onFilterChangeDebounced = useDebounce(onFilterChange, 200)

    return (
        <div style={{ display: "flex", justifyContent: "center", paddingTop: "2rem" }}>
            <div style={{ width: "50rem", gap: "0.5rem", display: "flex", flexDirection: "column" }}>
                <Autocomplete
                    freeSolo
                    options={Object.keys(configs)}
                    renderInput={(params) => <TextField {...params} label="Filter" />}
                    onInputChange={(_e, value) => onFilterChangeDebounced(value || "")}
                />
                <TableContainer component={Paper}>
                    <Table aria-label="simple table">
                        <TableHead>
                            <TableRow>
                                <TableCell> Key</TableCell>
                                <TableCell> Value </TableCell>
                            </TableRow>
                        </TableHead>
                        <TableBody>
                            {Object.entries(configs).filter(([key]) => key.toLowerCase().includes(filter)).map(([key, value]) => (
                                <TableRow
                                    key={key}
                                    sx={{ '&:last-child td, &:last-child th': { border: 0 } }}
                                >
                                    <TableCell component="th" scope="row"> {key} </TableCell>
                                    <TableCell> {value} </TableCell>
                                </TableRow>
                            ))}
                        </TableBody>
                    </Table>
                </TableContainer>
            </div>
        </div>
    )
};