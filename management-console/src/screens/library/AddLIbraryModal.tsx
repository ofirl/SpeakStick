import { useRef, useState } from "react";
import IconButton from "@mui/material/IconButton";
import Modal from "@mui/material/Modal";
import TextField from "@mui/material/TextField";
import Typography from "@mui/material/Typography";
import Box from "@mui/material/Box";
import Button from "@mui/material/Button";
import CircularProgress from "@mui/material/CircularProgress";
import Tooltip from "@mui/material/Tooltip";

import LibraryAddIcon from '@mui/icons-material/LibraryAdd';
import FolderCopyIcon from '@mui/icons-material/FolderCopy';

import { useCreateLibrary, useDuplicateLibrary } from "../../api/libraries";

const modalBoxStyle = {
    position: 'absolute',
    top: '50%',
    left: '50%',
    transform: 'translate(-50%, -50%)',
    width: "50%",
    maxWidth: 400,
    bgcolor: 'background.paper',
    border: '2px solid #000',
    boxShadow: 24,
    p: 4,
    display: "flex",
    flexDirection: "column",
    gap: "0.5rem"
};

type AddLibraryModalProps = {
    baseLibraryId?: number
}
export const AddLibraryModal = ({ baseLibraryId }: AddLibraryModalProps) => {
    const [modalOpen, setModalOpen] = useState(false);
    const nameRef = useRef<HTMLInputElement>(null)
    const descriptionRef = useRef<HTMLInputElement>(null)

    const { mutateAsync: createLibrary, isLoading: isCreatingLibrary } = useCreateLibrary();
    const { mutateAsync: duplicateLibrary, isLoading: isDuplicatingLibrary } = useDuplicateLibrary();
    const isLoading = isCreatingLibrary || isDuplicatingLibrary;

    const onSave = () => {
        if (!nameRef.current || !descriptionRef.current)
            return;

        let promise;
        if (baseLibraryId != null)
            promise = duplicateLibrary({ baseLibraryId, name: nameRef.current.value, description: descriptionRef.current.value })
        else
            promise = createLibrary({ name: nameRef.current.value, description: descriptionRef.current.value })

        promise.then(() => {
            setModalOpen(false)
        })
    };

    return (
        <>
            <Tooltip title="Add library">
                <IconButton
                    size="large"
                    color="inherit"
                    aria-label="add word"
                    onClick={() => setModalOpen(true)}
                >
                    {baseLibraryId ? <FolderCopyIcon /> : <LibraryAddIcon />}
                </IconButton>
            </Tooltip>
            <Modal
                open={modalOpen}
                onClose={() => setModalOpen(false)}
                aria-labelledby="modal-modal-title"
                aria-describedby="modal-modal-description"
            >
                <Box sx={modalBoxStyle}>
                    <Typography variant="h6" component="h2">
                        {
                            baseLibraryId ? "Duplicate" : "Create"
                        }
                        library
                    </Typography>
                    <TextField fullWidth label="Name" variant="outlined" inputRef={nameRef} />
                    <TextField fullWidth label="Description" variant="outlined" inputRef={descriptionRef} />
                    <Button disabled={isLoading} variant="contained" style={{ marginTop: "1rem", alignSelf: "end" }} onClick={onSave}>
                        {isLoading ? <CircularProgress /> : "Save"}
                    </Button>
                </Box>
            </Modal >
        </>
    )
};