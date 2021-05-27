import React from 'react';
import { makeStyles } from '@material-ui/core/styles';
import Button from '@material-ui/core/Button';
import IconButton from '@material-ui/core/IconButton';
import {upload} from '../../services/upload.service';
import CircularProgress from '@material-ui/core/CircularProgress';


const useStyles = makeStyles((theme) => ({
  root: {
    '& > *': {
      margin: theme.spacing(1),
    },
  },
  input: {
    display: 'none',
  },
}));

export default function UploadButtons(props) {
  const classes = useStyles();
  const { onClick, loading } = props;

  function onFileChange(event) {
      const file = event.target.files[0];
      const formData = new FormData();

      formData.append("csv", file, file.name);
      upload(formData)
  }

  return (
    <div className={classes.root}>
      <input
        // accept="image/*"
        className={classes.input}
        id="contained-button-file"
        multiple
        type="file"
        accept=".csv,.xlsx,.xls"
        onChange={onFileChange}
      />
      <label htmlFor="contained-button-file">
        <Button variant="contained" color= 'primary' component="span" onClick={onClick} disabled={loading}>
      {loading && <CircularProgress size={14} />}
      {!loading && 'import'}
    </Button>
      </label>
      <label htmlFor="icon-button-file">
        <IconButton color="primary" aria-label="upload picture" component="span">
        </IconButton>
      </label>
    </div>
  );
}
