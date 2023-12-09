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
import MoreVertIcon from '@mui/icons-material/MoreVert';

import { Library, useActivateLibrary, useDeleteLibrary, useGetLibraries } from "../../api/libraries";
import { useEffect, useRef, useState } from 'react';
import { Menu, MenuItem, Tooltip } from '@mui/material';
import { AddLibraryModal } from './AddLIbraryModal';
import { EditLibraryModal } from './EditLIbraryModal';

type LibraryControlsProps = {
  selectedLibrary: Library | undefined,
  onChange: (library: Library | undefined) => void
}
export const LibraryControls = ({ selectedLibrary, onChange }: LibraryControlsProps) => {
  const { data: libraries = [], isPending: isLoadingLibraries } = useGetLibraries();
  useEffect(() => {
    if (libraries && libraries.length > 0)
      onChange(libraries.find(l => l.active))
  }, [libraries, onChange]);

  const { mutateAsync: deleteLibrary, isPending: isDeletingLibrary } = useDeleteLibrary();
  const { mutateAsync: activateLibrary, isPending: isActivatingLibrary } = useActivateLibrary();

  const [menuOpen, setMenuOpen] = useState(false);
  const menuAnchorRef = useRef(null);

  const closeMenu = () => setMenuOpen(false);

  return (
    <div style={{ display: "flex", gap: "0.5rem" }}>
      {
        isLoadingLibraries ?
          <CircularProgress /> :
          <>
            <Autocomplete
              style={{ flexGrow: "1" }}
              sx={{ flexGrow: "1", }}
              value={selectedLibrary || libraries.find(l => l.active)}
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
              renderInput={(params) =>
                <>
                  <TextField {...params}
                    InputProps={{
                      ...params.InputProps, startAdornment:
                        <>
                          {!selectedLibrary?.editable && <LockIcon fontSize="small" />}
                          {selectedLibrary?.active && <CheckIcon fontSize="small" />}
                        </>
                    }}
                    label="Library"
                  />
                </>
              }
              onChange={(_e, value) => onChange(value)}
              disableClearable
              blurOnSelect
            />
            <Tooltip title="More actions">
              <IconButton
                size="large"
                color="inherit"
                aria-label="activate library"
                onClick={() => setMenuOpen(true)}
                ref={menuAnchorRef}
              >
                <MoreVertIcon />
              </IconButton>
            </Tooltip>
            <Menu
              id="long-menu"
              MenuListProps={{
                'aria-labelledby': 'long-button',
              }}
              anchorEl={menuAnchorRef.current}
              open={menuOpen}
              onClose={() => closeMenu()}
            >
              <EditLibraryModal closeMenu={closeMenu} libraryId={selectedLibrary?.id} disabled={!selectedLibrary?.editable} />
              <AddLibraryModal closeMenu={closeMenu} />
              <MenuItem
                disabled={isActivatingLibrary || selectedLibrary?.active}
                onClick={() => {
                  selectedLibrary && activateLibrary({ libraryId: selectedLibrary.id }).then(() => {
                    closeMenu();
                  })
                }}
                sx={{ gap: "0.5rem" }}
                disableRipple
              >
                <FolderSpecialIcon />
                Activate
              </MenuItem>
              <AddLibraryModal closeMenu={closeMenu} baseLibraryId={selectedLibrary?.id} />
              <MenuItem
                disabled={!selectedLibrary || isDeletingLibrary || selectedLibrary.active || !selectedLibrary.editable}
                onClick={() => {
                  selectedLibrary && deleteLibrary({ libraryId: selectedLibrary.id }).then(() => {
                    closeMenu();
                  });
                }}
                sx={{ gap: "0.5rem" }}
                disableRipple
              >
                {isDeletingLibrary ? <CircularProgress /> : <FolderDeleteIcon />}
                Delete
              </MenuItem>
            </Menu>
          </>
      }
    </div >
  )
};