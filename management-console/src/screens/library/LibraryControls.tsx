import CircularProgress from '@mui/material/CircularProgress';
import Autocomplete from '@mui/material/Autocomplete';
import Box from '@mui/material/Box';
import Typography from '@mui/material/Typography';
import IconButton from '@mui/material/IconButton';
import TextField from '@mui/material/TextField';

import LockIcon from '@mui/icons-material/Lock';
import FolderDeleteIcon from '@mui/icons-material/FolderDelete';
import FolderSpecialIcon from '@mui/icons-material/FolderSpecial';
import CheckIcon from '@mui/icons-material/Check';

import { Library, useDeleteLibrary, useGetLibraries } from "../../api/libraries";
import { useEffect } from 'react';
import { Tooltip } from '@mui/material';
import { AddLibraryModal } from './AddLIbraryModal';

type LibraryControlsProps = {
    selectedLibrary: Library | undefined,
    onChange: (library: Library | undefined) => void
}
export const LibraryControls = ({ selectedLibrary, onChange }: LibraryControlsProps) => {
    const { data: libraries = [], isLoading: isLoadingLibraries } = useGetLibraries();
    useEffect(() => {
        if (libraries && libraries.length > 0)
            onChange(libraries.find(l => l.active))
    }, [libraries, onChange])

    const { mutateAsync: deleteLibrary, isLoading: isDeletingLibrary } = useDeleteLibrary();

    return (
        <div style={{ display: "flex", gap: "0.5rem" }}>
            {
                isLoadingLibraries ?
                    <CircularProgress /> :
                    <>
                        <Autocomplete
                            style={{ flexGrow: "1" }}
                            sx={{ flexGrow: "1", }}
                            defaultValue={libraries.find(l => l.active)}
                            getOptionLabel={(option) => typeof option === "string" ? option : option.name}
                            options={libraries}
                            renderOption={(props, option) => (
                                <Box component="li" sx={{
                                    "&.MuiAutocomplete-option": {
                                        alignItems: "center",
                                        gap: "0.5rem"
                                    }
                                }} {...props}>
                                    {!option.editable &&
                                        <div>
                                            <LockIcon fontSize="medium" />
                                        </div>
                                    }
                                    <div style={{ display: "flex", flexDirection: "column", flexGrow: "1" }}>
                                        <Typography variant='body2'>
                                            {option.name}
                                        </Typography>
                                        <Typography variant='caption'>
                                            {option.description}
                                        </Typography>
                                    </div>
                                    {option.active &&
                                        <div>
                                            <CheckIcon fontSize="medium" />
                                        </div>
                                    }
                                </Box>
                            )}
                            renderInput={(params) => <> <TextField {...params} InputProps={{ ...params.InputProps, startAdornment: !selectedLibrary?.editable && <LockIcon fontSize="small" /> }} label="Library" /> </>}
                            onChange={(_e, value) => onChange(value)}
                            disableClearable
                            blurOnSelect
                        />
                        <AddLibraryModal />
                        <Tooltip title="Activate library">
                            <IconButton
                                size="large"
                                color="inherit"
                                aria-label="activate library"
                            >
                                <FolderSpecialIcon />
                            </IconButton>
                        </Tooltip>
                        <AddLibraryModal baseLibraryId={selectedLibrary?.id} />
                        <Tooltip title="Delete library">
                            <IconButton
                                disabled={!selectedLibrary || !isDeletingLibrary}
                                size="large"
                                color="inherit"
                                aria-label="delete library"
                                onClick={() => selectedLibrary && deleteLibrary({ libraryId: selectedLibrary.id })}
                            >
                                {isDeletingLibrary ? <CircularProgress /> : <FolderDeleteIcon />}
                            </IconButton>
                        </Tooltip>
                    </>
            }
        </div >
    )
};