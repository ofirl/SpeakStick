import Table from '@mui/material/Table';
import TableBody from '@mui/material/TableBody';
import TableCell from '@mui/material/TableCell';
import TableContainer from '@mui/material/TableContainer';
import TableHead from '@mui/material/TableHead';
import TableRow from '@mui/material/TableRow';
import Paper from '@mui/material/Paper';
import TextField from '@mui/material/TextField';
import Autocomplete from '@mui/material/Autocomplete';

import { useCallback, useState } from 'react';
import { useDebounce } from '../../customHooks/useDebounce';
import { useGetWords } from '../../api/words';

export const Words = () => {
    const [filter, setFilter] = useState("");
    const { data: words = {} } = useGetWords();
    console.log(words)

    const onFilterChange = useCallback((value: string) => {
        setFilter(value.toLowerCase())
    }, [])
    const onFilterChangeDebounced = useDebounce(onFilterChange, 200)

    return (
        <div style={{ display: "flex", justifyContent: "center", paddingTop: "2rem" }}>
            <div style={{ width: "50rem", gap: "0.5rem", display: "flex", flexDirection: "column" }}>
                <Autocomplete
                    freeSolo
                    options={Array.from(new Set([...Object.keys(words), ...Object.values(words)]))}
                    renderInput={(params) => <TextField {...params} label="Filter" />}
                    onInputChange={(_e, value) => onFilterChangeDebounced(value || "")}
                />
                <TableContainer component={Paper}>
                    <Table aria-label="simple table">
                        <TableHead>
                            <TableRow>
                                <TableCell> Positions </TableCell>
                                <TableCell> Word </TableCell>
                            </TableRow>
                        </TableHead>
                        <TableBody>
                            {Object.entries(words).filter(([positions, word]) =>
                                positions.toLowerCase().includes(filter) ||
                                word.toLowerCase().includes(filter))
                                .map(([positions, word]) => (
                                    <TableRow
                                        key={positions}
                                        sx={{ '&:last-child td, &:last-child th': { border: 0 } }}
                                    >
                                        <TableCell component="th" scope="row"> {positions} </TableCell>
                                        <TableCell> {word} </TableCell>
                                    </TableRow>
                                ))}
                        </TableBody>
                    </Table>
                </TableContainer>
            </div>
        </div>
    )
};