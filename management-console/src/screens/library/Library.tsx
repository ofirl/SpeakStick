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
import { useDeleteLibraryItem, useGetLibraryItems } from '../../api/libraryItems';
import { AddWordModal } from './AddLibraryItemModal';
import IconButton from '@mui/material/IconButton';
import DeleteIcon from '@mui/icons-material/Delete';
// import { useGetLibraries } from '../../api/libraries';

export const Library = () => {
    const [filter, setFilter] = useState("");
    // const { data: libraries } = useGetLibraries();
    const [selectedLibrary] = useState(0);
    const { data: libraryItems = [], isLoading } = useGetLibraryItems(selectedLibrary);

    const onFilterChange = useCallback((value: string) => {
        setFilter(value.toLowerCase())
    }, [])
    const onFilterChangeDebounced = useDebounce(onFilterChange, 200)

    const { mutateAsync: deletePosition, isLoading: isDeleting } = useDeleteLibraryItem();

    return (
        <div style={{ maxWidth: "50rem", gap: "0.5rem", display: "flex", flexDirection: "column", height: "100%", flexGrow: 1 }}>
            <div style={{ display: "flex", gap: "0.5rem" }}>
                <Autocomplete
                    style={{ flexGrow: "1" }}
                    freeSolo
                    options={Array.from(new Set([...Object.keys(libraryItems), ...Object.values(libraryItems)]))}
                    renderInput={(params) => <TextField {...params} label="Filter" />}
                    onInputChange={(_e, value) => onFilterChangeDebounced(value || "")}
                />
                <AddWordModal libraryId={selectedLibrary} />
            </div>
            <TableContainer component={Paper}>
                <Table aria-label="simple table">
                    <TableHead>
                        <TableRow>
                            <TableCell sx={(theme) => ({ width: window.innerWidth < theme.breakpoints.values.sm ? "4rem" : "6rem", background: "white" })}> Positions </TableCell>
                            <TableCell sx={{ background: "white" }}> Word </TableCell>
                            <TableCell sx={{ width: "3rem", background: "white" }} />
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
                            libraryItems.filter(({ positions, word }) =>
                                positions.toString().toLowerCase().includes(filter) ||
                                word.toLowerCase().includes(filter))
                                .map(({ positions, word }) => (
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
                                                onClick={() => deletePosition({ libraryId: selectedLibrary, position: positions.toString() })}
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
    )
};