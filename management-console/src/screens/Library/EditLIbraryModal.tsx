import { useMemo, useRef, useState } from "react";
import Modal from "@mui/material/Modal";
import TextField from "@mui/material/TextField";
import Typography from "@mui/material/Typography";
import Box from "@mui/material/Box";
import Button from "@mui/material/Button";
import CircularProgress from "@mui/material/CircularProgress";

import EditIcon from '@mui/icons-material/Edit';

import { useEditLibrary, useGetLibraries } from "../../api/libraries";
import MenuItem from "@mui/material/MenuItem";

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

type EditLibraryModalProps = {
  libraryId?: number,
  disabled?: boolean
  closeMenu: () => void
}
export const EditLibraryModal = ({ libraryId, closeMenu, disabled }: EditLibraryModalProps) => {
  const [modalOpen, setModalOpen] = useState(false);
  const [libraryName, setLibraryName] = useState("");
  const descriptionRef = useRef<HTMLInputElement>(null);

  const { data: libraries = [] } = useGetLibraries();
  const nameError = useMemo(() =>
    libraries.find(l => l.name === libraryName) != null ? "Name already exists" : ""
    , [libraries, libraryName]);

  const { mutateAsync: updateLibrary, isPending: isUpdatingLibrary } = useEditLibrary();

  const onSave = () => {
    if (libraryId == null || !libraryName || !descriptionRef.current)
      return;

    updateLibrary({ libraryId: libraryId, name: libraryName, description: descriptionRef.current.value }).then(() => {
      setModalOpen(false);
      closeMenu();
    })
  };

  return (
    <>
      <MenuItem
        disabled={disabled}
        onClick={() => setModalOpen(true)}
        sx={{ gap: "0.5rem" }}
        disableRipple
      >
        <EditIcon />
        Edit
      </MenuItem>
      <Modal
        open={modalOpen}
        onClose={() => setModalOpen(false)}
      >
        <Box sx={modalBoxStyle}>
          <Typography variant="h6" component="h2">
            Edit library
          </Typography>
          <TextField fullWidth
            label="Name"
            variant="outlined"
            value={libraryName}
            onInput={(e) => setLibraryName((e.target as HTMLInputElement).value)}
            error={!!nameError}
            helperText={nameError || undefined}
          />
          <TextField fullWidth label="Description" variant="outlined" inputRef={descriptionRef} />
          <Button disabled={isUpdatingLibrary || !!nameError} variant="contained" style={{ marginTop: "1rem", alignSelf: "end" }} onClick={onSave}>
            {isUpdatingLibrary ? <CircularProgress /> : "Save"}
          </Button>
        </Box>
      </Modal >
    </>
  )
};