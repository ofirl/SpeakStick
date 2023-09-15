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
import { Library as LibraryT } from '../../api/libraries';
import { LibraryControls } from './LibraryControls';

export const Library = () => {
    const [filter, setFilter] = useState("");
    const [selectedLibrary, setSelectedLibrary] = useState<LibraryT | undefined>();

    const { data: libraryItems = [], isLoading } = useGetLibraryItems(selectedLibrary?.id);

    const onFilterChange = useCallback((value: string) => {
        setFilter(value.toLowerCase())
    }, [])
    const onFilterChangeDebounced = useDebounce(onFilterChange, 200)

    const { mutateAsync: deletePosition, isLoading: isDeleting } = useDeleteLibraryItem();

    return (
        <div style={{ maxWidth: "50rem", gap: "0.5rem", display: "flex", flexDirection: "column", height: "100%", flexGrow: 1 }}>
            <LibraryControls selectedLibrary={selectedLibrary} onChange={setSelectedLibrary} />
            <div style={{ display: "flex", gap: "0.5rem" }}>
                <Autocomplete
                    style={{ flexGrow: "1" }}
                    freeSolo
                    // options={Array.from(new Set(libraryItems.flatMap(i => [{ value: i.positions.toString(), label: `Positions: ${i.positions}` }, { value: i.word, label: `Word: ${i.word}` }])))}
                    options={Array.from(new Set(libraryItems.flatMap(i => [i.positions.toString(), i.word])))}
                    renderInput={(params) => <TextField {...params} label="Filter" />}
                    onInputChange={(_e, value) => { console.log(value); onFilterChangeDebounced(value || "") }}
                />
                <AddWordModal libraryId={selectedLibrary?.id || 1} />
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
                                                disabled={isDeleting || !selectedLibrary}
                                                size="large"
                                                color="inherit"
                                                aria-label="delete word"
                                                onClick={() => selectedLibrary && deletePosition({ libraryId: selectedLibrary.id, position: positions.toString() })}
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