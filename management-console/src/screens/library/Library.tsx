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
import CircularProgress from '@mui/material/CircularProgress';

import { useCallback, useState } from 'react';
import { useDebounce } from '../../customHooks/useDebounce';
import { useDeletePosition, useGetPositions } from '../../api/positions';
import { AddWordModal } from './AddPositionModal';
import IconButton from '@mui/material/IconButton';
import DeleteIcon from '@mui/icons-material/Delete';

export const Library = () => {
    const [filter, setFilter] = useState("");
    const { data: positions = {}, isLoading } = useGetPositions();

    const onFilterChange = useCallback((value: string) => {
        setFilter(value.toLowerCase())
    }, [])
    const onFilterChangeDebounced = useDebounce(onFilterChange, 200)

    const { mutateAsync: deletePosition, isLoading: isDeleting } = useDeletePosition();

    return (
        <div style={{ display: "flex", justifyContent: "center", paddingTop: "2rem" }}>
            <div style={{ width: "50rem", gap: "0.5rem", display: "flex", flexDirection: "column" }}>
                <div style={{ display: "flex", gap: "0.5rem" }}>
                    <Autocomplete
                        style={{ flexGrow: "1" }}
                        freeSolo
                        options={Array.from(new Set([...Object.keys(positions), ...Object.values(positions)]))}
                        renderInput={(params) => <TextField {...params} label="Filter" />}
                        onInputChange={(_e, value) => onFilterChangeDebounced(value || "")}
                    />
                    <AddWordModal />
                </div>
                <TableContainer component={Paper}>
                    <Table aria-label="simple table">
                        <TableHead>
                            <TableRow>
                                <TableCell width={"45%"}> Positions </TableCell>
                                <TableCell width={"45%"}> Word </TableCell>
                                <TableCell />
                            </TableRow>
                        </TableHead>
                        <TableBody>
                            {isLoading ?
                                [1, 2].map(i => (
                                    <TableRow
                                        key={"row" + i}
                                        sx={{ '&:last-child td, &:last-child th': { border: 0 } }}
                                    >
                                        <TableCell colSpan={3} component="th" scope="row">
                                            <Skeleton variant="rounded" height={"2rem"} />
                                        </TableCell>
                                    </TableRow>
                                ))
                                :
                                Object.entries(positions).filter(([positions, word]) =>
                                    positions.toLowerCase().includes(filter) ||
                                    word.toLowerCase().includes(filter))
                                    .map(([positions, word]) => (
                                        <TableRow
                                            key={positions}
                                            sx={{ '&:last-child td, &:last-child th': { border: 0 } }}
                                        >
                                            <TableCell component="th" scope="row"> {positions} </TableCell>
                                            <TableCell> {word} </TableCell>
                                            <TableCell>
                                                <IconButton
                                                    disabled={isDeleting}
                                                    size="large"
                                                    color="inherit"
                                                    aria-label="delete word"
                                                    onClick={() => deletePosition({ position: positions })}
                                                >
                                                    {isDeleting ? <CircularProgress /> : <DeleteIcon />}
                                                </IconButton>
                                            </TableCell>
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