import React from 'react';
import { makeStyles } from '@material-ui/core/styles';
import Button from '@material-ui/core/Button';
import {getContents} from "../../services/content.service";

const useStyles = makeStyles((theme) => ({
  root: {
    '& > *': {
      margin: theme.spacing(1),
    },
  },
}));

function getRandomInt(max) {
  return Math.floor(Math.random() * max);
}

export default function ContainedButtons() {
  const classes = useStyles();
  const [data, setData] = React.useState(null);

  React.useEffect(() => {
    if (data)
      window.location = "/document/" + data.id;
    }, [data]);


  const handleClick = () => {
    getContents('/random/', {}, setData)
  }

  return (
    <div className={classes.root}>
      <Button variant="contained" color="primary" onClick = {handleClick}>
        Random
      </Button>
    </div>
  );
}
