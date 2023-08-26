import { useRef, useState } from 'react';

import Typography from '@mui/material/Typography';
import Modal from '@mui/material/Modal';
import IconButton from '@mui/material/IconButton';
import Box from '@mui/material/Box';
import AddIcon from '@mui/icons-material/Add';
import TextField from '@mui/material/TextField';
import InputLabel from '@mui/material/InputLabel';
import Select from '@mui/material/Select';
import MenuItem from '@mui/material/MenuItem';
import Button from '@mui/material/Button';
import CircularProgress from '@mui/material/CircularProgress';
import { useGetFiles, useUpdateWord } from '../../api/words';

const style = {
    position: 'absolute',
    top: '50%',
    left: '50%',
    transform: 'translate(-50%, -50%)',
    width: 400,
    bgcolor: 'background.paper',
    border: '2px solid #000',
    boxShadow: 24,
    p: 4,
    display: "flex",
    flexDirection: "column"
};

export const AddWordModal = () => {
    const [modalOpen, setModalOpen] = useState(false);
    const positionsRef = useRef<HTMLInputElement>(null)
    const wordRef = useRef<HTMLSelectElement>(null)
    const { data: files } = useGetFiles();

    const { mutateAsync: updateWord, isLoading } = useUpdateWord();

    const onSave = () => {
        if (!positionsRef.current || !wordRef.current)
            return;

        updateWord({ position: positionsRef.current.value, word: wordRef.current.value }).then(() => {
            setModalOpen(false)
        })
    };

    return (
        <>
            <IconButton
                size="large"
                color="inherit"
                aria-label="add word"
                onClick={() => setModalOpen(true)}
            >
                <AddIcon />
            </IconButton>
            <Modal
                open={modalOpen}
                onClose={() => setModalOpen(false)}
                aria-labelledby="modal-modal-title"
                aria-describedby="modal-modal-description"
            >
                <Box sx={style}>
                    <Typography variant="h6" component="h2">
                        Add word
                    </Typography>
                    <TextField fullWidth label="Positions" variant="outlined" inputRef={positionsRef} />
                    <InputLabel id="word-label">Word</InputLabel>
                    <Select
                        fullWidth
                        labelId="word-label"
                        label="Word"
                        inputRef={wordRef}
                    >
                        {
                            files?.map(file => (
                                <MenuItem value={file}>{file}</MenuItem>
                            ))
                        }
                    </Select>
                    <Button disabled={isLoading} variant="contained" style={{ marginTop: "1rem", alignSelf: "end" }} onClick={onSave}>
                        {isLoading ? <CircularProgress /> : "Save"}
                    </Button>
                </Box>
            </Modal >
        </>
    )
};