import Table from '@mui/material/Table';
import TableBody from '@mui/material/TableBody';
import TableCell from '@mui/material/TableCell';
import TableContainer from '@mui/material/TableContainer';
import TableHead from '@mui/material/TableHead';
import TableRow from '@mui/material/TableRow';
import Paper from '@mui/material/Paper';
import TextField from '@mui/material/TextField';
import Autocomplete from '@mui/material/Autocomplete';
import Skeleton from '@mui/material/Skeleton';

import { useGetConfigs, useUpdateConfig } from "../../api/configs";
import { useCallback, useState } from 'react';
import { useDebounce } from '../../customHooks/useDebounce';
import { ValueCell } from './ValueCell';

export const Settings = () => {
    const [filter, setFilter] = useState("");
    const { data: configs = {}, isLoading } = useGetConfigs();

    const { mutate: updateConfig } = useUpdateConfig();

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
                                <TableCell width={"50%"}> Key</TableCell>
                                <TableCell> Value </TableCell>
                            </TableRow>
                        </TableHead>
                        <TableBody>
                            {isLoading ?
                                [
                                    <TableRow
                                        key={"positions"}
                                        sx={{ '&:last-child td, &:last-child th': { border: 0 } }}
                                    >
                                        <TableCell colSpan={2} component="th" scope="row">
                                            <Skeleton variant="rounded" height={"2rem"} />
                                        </TableCell>
                                    </TableRow>,
                                    <TableRow
                                        key={"word"}
                                        sx={{ '&:last-child td, &:last-child th': { border: 0 } }}
                                    >
                                        <TableCell colSpan={2} component="th" scope="row">
                                            <Skeleton variant="rounded" height={"2rem"} />
                                        </TableCell>
                                    </TableRow>
                                ]
                                :
                                Object.entries(configs).filter(([key]) => key.toLowerCase().includes(filter)).map(([key, value]) => (
                                    <TableRow
                                        key={key}
                                        sx={{ '&:last-child td, &:last-child th': { border: 0 } }}
                                    >
                                        <TableCell component="th" scope="row"> {key} </TableCell>
                                        <TableCell> <ValueCell value={value} onEdit={(updatedValue) => updateConfig({ key, value: updatedValue })} /> </TableCell>
                                    </TableRow>
                                ))
                            }
                        </TableBody>
                    </Table>
                </TableContainer>
            </div>
        </div>
    )
};