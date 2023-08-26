import { CSSProperties } from "react";
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

import { ComponentProps, useCallback, useState } from 'react';
import { useDebounce } from '../../customHooks/useDebounce';
import IconButton from '@mui/material/IconButton';
import DeleteIcon from '@mui/icons-material/Delete';
import { useDeleteWord, useGetWords, useUploadWord } from '../../api/words';
import { useGetPositions } from '../../api/positions';
import { DeleteWordModal } from './DeleteWordModal';
import CloudUploadIcon from '@mui/icons-material/CloudUpload';

import Button from '@mui/material/Button';

const VisuallyHiddenInputStyle: CSSProperties = {
    clip: "rect(0 0 0 0)",
    clipPath: "inset(50%)",
    height: "1px",
    overflow: "hidden",
    position: "absolute",
    bottom: "0",
    left: "0",
    whiteSpace: "nowrap",
    width: "1px"
};

export const Words = () => {
    const [filter, setFilter] = useState("");
    const [deleteConfirmationOpen, setDeleteConfirmationOpen] = useState(false);
    const { data: words = [], isLoading } = useGetWords();

    const [deletionModalProps, setDeletionModalProps] = useState<Omit<ComponentProps<typeof DeleteWordModal>, "open" | "onDecline">>({} as ComponentProps<typeof DeleteWordModal>);

    const onFilterChange = useCallback((value: string) => {
        setFilter(value.toLowerCase());
    }, [])
    const onFilterChangeDebounced = useDebounce(onFilterChange, 200)

    const { mutateAsync: uploadWord, isLoading: isUploading } = useUploadWord();
    const { mutateAsync: deleteWord, isLoading: isDeleting } = useDeleteWord();
    const { data: positions = {} } = useGetPositions();

    const onDeleteWord = (word: string) => {
        const wordPositions = Object.entries(positions).filter(([, positionWord]) => positionWord === word).map(([position]) => position);
        if (wordPositions.length === 0) {
            deleteWord({ word });
            return;
        }
        setDeletionModalProps({
            onApprove: () => deleteWord({ word }),
            positions: wordPositions,
            word: word
        });
        setDeleteConfirmationOpen(true);
    };

    const onFileSelect: React.ChangeEventHandler<HTMLInputElement> = (e) => {
        const selecteFile = e.target.files?.[0];
        if (!selecteFile)
            return null;
        // Create an object of formData
        // const formData = new FormData();

        // Update the formData object
        // formData.append(
        //     "file",
        //     selecteFile,
        //     selecteFile.name
        // );

        uploadWord({ file: selecteFile, fileName: selecteFile.name })
    }


    return (
        <div style={{ display: "flex", justifyContent: "center", paddingTop: "2rem" }}>
            <div style={{ width: "50rem", gap: "0.5rem", display: "flex", flexDirection: "column" }}>
                <div style={{ display: "flex", gap: "0.5rem" }}>
                    <Autocomplete
                        style={{ flexGrow: "1" }}
                        freeSolo
                        options={words}
                        renderInput={(params) => <TextField {...params} label="Filter" />}
                        onInputChange={(_e, value) => onFilterChangeDebounced(value || "")}
                    />
                    <DeleteWordModal open={deleteConfirmationOpen} onDecline={() => setDeleteConfirmationOpen(false)} {...deletionModalProps} />
                    <Button
                        component="label"
                        variant="outlined"
                        startIcon={<CloudUploadIcon />}
                    >
                        {
                            isUploading ? <CircularProgress /> :
                                <>
                                    Upload a file
                                    <input style={VisuallyHiddenInputStyle} onChange={onFileSelect} type="file" />
                                </>
                        }
                    </Button>
                </div>
                <TableContainer component={Paper}>
                    <Table aria-label="simple table">
                        <TableHead>
                            <TableRow>
                                <TableCell width={"90%"}> Word </TableCell>
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
                                        <TableCell colSpan={2} component="th" scope="row">
                                            <Skeleton variant="rounded" height={"2rem"} />
                                        </TableCell>
                                    </TableRow>
                                ))
                                :
                                words.filter((word) => word.toLowerCase().includes(filter))
                                    .map((word) => (
                                        <TableRow
                                            key={word}
                                            sx={{ '&:last-child td, &:last-child th': { border: 0 } }}
                                        >
                                            <TableCell component="th" scope="row"> {word} </TableCell>
                                            <TableCell>
                                                <IconButton
                                                    disabled={isDeleting}
                                                    size="large"
                                                    color="inherit"
                                                    aria-label="delete word"
                                                    onClick={() => onDeleteWord(word)}
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