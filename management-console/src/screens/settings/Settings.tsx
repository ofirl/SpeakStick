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
import { DefaultValueCell } from './DefaultValueCell';
import { Typography } from '@mui/material';

export const Settings = () => {
    const [filter, setFilter] = useState("");
    const { data: configs = [], isLoading } = useGetConfigs();

    const { mutateAsync: updateConfig } = useUpdateConfig();

    const onFilterChange = useCallback((value: string) => {
        setFilter(value.toLowerCase())
    }, [])
    const onFilterChangeDebounced = useDebounce(onFilterChange, 200)

    return (
        <div style={{ maxWidth: "70rem", gap: "0.5rem", display: "flex", flexDirection: "column", height: "100%", width: "100%" }}>
            <Autocomplete
                freeSolo
                options={configs.map(c => c.key)}
                renderInput={(params) => <TextField {...params} label="Filter" />}
                onInputChange={(_e, value) => onFilterChangeDebounced(value || "")}
            />
            <TableContainer component={Paper}>
                <Table aria-label="simple table">
                    <TableHead>
                        <TableRow>
                            <TableCell sx={{ width: "1rem" }}> Key</TableCell>
                            <TableCell sx={(theme) => ({ width: window.innerWidth < theme.breakpoints.values.sm ? "5rem" : "6rem" })}> Value </TableCell>
                            <TableCell sx={(theme) => ({ width: window.innerWidth < theme.breakpoints.values.sm ? "5rem" : "6rem" })}> Default Value </TableCell>
                        </TableRow>
                    </TableHead>
                    <TableBody>
                        {isLoading ?
                            [
                                <TableRow
                                    key={"positions"}
                                    sx={{ '&:last-child td, &:last-child th': { border: 0 } }}
                                >
                                    <TableCell colSpan={2} scope="row">
                                        <Skeleton variant="rounded" height={"2rem"} />
                                    </TableCell>
                                </TableRow>,
                                <TableRow
                                    key={"word"}
                                    sx={{ '&:last-child td, &:last-child th': { border: 0 } }}
                                >
                                    <TableCell colSpan={2} scope="row">
                                        <Skeleton variant="rounded" height={"2rem"} />
                                    </TableCell>
                                </TableRow>
                            ]
                            :
                            configs.filter((c) => c.key.toLowerCase().includes(filter)).map((c) => (
                                <TableRow
                                    key={c.key}
                                    sx={{ '&:last-child td, &:last-child th': { border: 0 } }}
                                >
                                    <TableCell scope="row"> <Typography variant="body2" sx={{ wordBreak: "break-word" }}> {c.key} </Typography> <Typography variant="caption"> {c.description} </Typography> </TableCell>
                                    <TableCell> <ValueCell value={c.value} onEdit={(updatedValue) => updateConfig({ key: c.key, value: updatedValue })} /> </TableCell>
                                    <TableCell>
                                        <DefaultValueCell value={c.default_value} onRestore={() => updateConfig({ key: c.key, value: c.default_value })} />
                                    </TableCell>
                                </TableRow>
                            ))
                        }
                    </TableBody>
                </Table>
            </TableContainer>
        </div>
    )
};