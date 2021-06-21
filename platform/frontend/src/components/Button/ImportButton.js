import React from 'react';
import {makeStyles} from '@material-ui/core/styles';
import Button from '@material-ui/core/Button';

import {upload} from '../../services/upload.service';
import CircularProgress from '@material-ui/core/CircularProgress';


import {green} from '@material-ui/core/colors';

const useStyles = makeStyles((theme) => ({
    root: {
        '& > *': {
            margin: theme.spacing(1),
        },
    },
    input: {
        display: 'none',
    },
    wrapper: {
        margin: theme.spacing(1),
        position: 'relative',
    },
    buttonProgress: {
        color: green[500],
        position: 'absolute',
        top: '50%',
        left: '50%',
        marginTop: -12,
        marginLeft: -12,
    },

}));

export default function UploadButtons() {
    const classes = useStyles();
    const [loading, setLoading] = React.useState(false);


    function onFileChange(event) {
        setLoading(true)
        const file = event.target.files[0]
        const formData = new FormData()
        formData.append("csv", file, file.name);
        upload(formData, () => {
            setLoading(false);
            // window.location = window.location
        });
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
                disabled={loading}
            />
            <label htmlFor="contained-button-file" className={classes.wrapper}>
                {/*<Button variant="contained" color="primary" component="span">
          Import
        </Button>*/}
                <Button
                    variant="contained"
                    color="primary"
                    disabled={loading}
                    component="span"
                >
                    Import
                </Button>
                {loading && <CircularProgress size={24} className={classes.buttonProgress}/>}
            </label>
        </div>
    );
}
