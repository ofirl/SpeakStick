import { useMemo, useRef, useState } from "react";
import { styled } from '@mui/material/styles';
import Modal from "@mui/material/Modal";
import TextField from "@mui/material/TextField";
import Typography from "@mui/material/Typography";
import Box from "@mui/material/Box";
import Button from "@mui/material/Button";
import CircularProgress from "@mui/material/CircularProgress";

import LibraryAddIcon from '@mui/icons-material/LibraryAdd';
import FolderCopyIcon from '@mui/icons-material/FolderCopy';
import CloudUploadIcon from '@mui/icons-material/CloudUpload';

import { useCreateLibrary, useDuplicateLibrary, useGetLibraries, useImportLibrary } from "../../api/libraries";
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

const VisuallyHiddenInput = styled('input')({
  clip: 'rect(0 0 0 0)',
  clipPath: 'inset(50%)',
  height: 1,
  overflow: 'hidden',
  position: 'absolute',
  bottom: 0,
  left: 0,
  whiteSpace: 'nowrap',
  width: 1,
});

type AddLibraryModalProps = {
  baseLibraryId?: number,
  libraryPath?: string,
  closeMenu: () => void
}
export const AddLibraryModal = ({ baseLibraryId, libraryPath, closeMenu }: AddLibraryModalProps) => {
  const [modalOpen, setModalOpen] = useState(false);
  const [libraryName, setLibraryName] = useState("");
  const descriptionRef = useRef<HTMLInputElement>(null);

  const { data: libraries = [] } = useGetLibraries();
  const nameError = useMemo(() =>
    libraries.find(l => l.name === libraryName) != null ? "Name already exists" : ""
    , [libraries, libraryName]);

  const { mutateAsync: createLibrary, isPending: isCreatingLibrary } = useCreateLibrary();
  const { mutateAsync: duplicateLibrary, isPending: isDuplicatingLibrary } = useDuplicateLibrary();
  const { mutateAsync: importLibrary, isPending: isImportingLibrary } = useImportLibrary();
  const isLoading = isCreatingLibrary || isDuplicatingLibrary || isImportingLibrary;

  const onSave = () => {
    if (!libraryName || !descriptionRef.current)
      return;

    let promise;
    if (baseLibraryId != null) {
      promise = duplicateLibrary({ baseLibraryId, name: libraryName, description: descriptionRef.current.value });
    } else if (libraryPath != null) {
      //libraryFile = file-content from libraryPath
      promise = importLibrary({ name: libraryName, description: descriptionRef.current.value, libraryFile: "" });
    } else {
      promise = createLibrary({ name: libraryName, description: descriptionRef.current.value });
    }

    promise.then(() => {
      setModalOpen(false);
      closeMenu();
    })
  };

  return (
    <>
      <MenuItem
        onClick={() => setModalOpen(true)}
        sx={{ gap: "0.5rem" }}
        disableRipple
      >
        {baseLibraryId ? <FolderCopyIcon /> : <LibraryAddIcon />}
        {baseLibraryId ? "Duplicate" : "Create"}
      </MenuItem>
      <Modal
        open={modalOpen}
        onClose={() => setModalOpen(false)}
      >
        <Box sx={modalBoxStyle}>
          <Typography variant="h6" component="h2">
            {
              baseLibraryId ? "Duplicate" : "Create"
            }
            {" "}
            library
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
          <Button component="label" variant="contained" startIcon={<CloudUploadIcon />}>
            Upload file
            <VisuallyHiddenInput type="file" accept=".zip" value={libraryPath}/>
          </Button>
          <Button disabled={isLoading || !!nameError} variant="contained" style={{ marginTop: "1rem", alignSelf: "end" }} onClick={onSave}>
            {isLoading ? <CircularProgress /> : "Save"}
          </Button>
        </Box>
      </Modal>
    </>
  )
};