import React from 'react';
import clsx from 'clsx';
import {makeStyles} from '@material-ui/core/styles';
import Box from '@material-ui/core/Box';
import Container from '@material-ui/core/Container';
import Grid from '@material-ui/core/Grid';
import Paper from '@material-ui/core/Paper';
import Header from "../components/Header";
import Footer from "../components/Footer"
import Button from '@material-ui/core/Button';
import Select from '@material-ui/core/Select';
import InputLabel from '@material-ui/core/InputLabel';
import MenuItem from '@material-ui/core/MenuItem';
import FormControl from '@material-ui/core/FormControl';
import Typography from '@material-ui/core/Typography';
import ProjectEditor from "../components/ProjectEditor";
import FormGroup from '@material-ui/core/FormGroup';




const projects = [{name: 'PET', nbDocument: 10}, {name: 'DIM', nbDocument: 10}]

const useStyles = makeStyles((theme) => ({
    root: {
        // display: 'flex',
    },
    appBarSpacer: theme.mixins.toolbar,
    // // content: {
    // //     flexGrow: 1,
    // //     height: '100vh',
    // //     overflow: 'auto',
    // //     paddingRight: 24,
    // // },
    // container: {
    //     paddingTop: theme.spacing(4),
    //     paddingBottom: theme.spacing(4),
    // },
    // paper: {
    //     padding: theme.spacing(2),
    //     display: 'flex',
    //     overflow: 'auto',
    //     flexDirection: 'column',
    // },
    
    // form: {
    //     // display: 'flex',
    //     // flexDirection: 'column',
    //   },
    formControl: {
      margin: theme.spacing(1),
      minWidth: 120,
    }
}));

export default function Dashboard() {
    const classes = useStyles();
    // const [open, setOpen] = React.useState(true);
    const fixedHeightPaper = clsx(classes.paper, classes.fixedHeight);

    const [selectedProject, setSelectedProject] =  React.useState (-1)

    

    return (

        <div>
            <Header/>
            <div className={classes.appBarSpacer}/>
            <main className={classes.content}>
                <Container maxWidth="lg" className={classes.container}>

                    <form className={classes.form} noValidate>
                        <FormGroup row>
                            <FormControl className={classes.formControl}> 
                                <Button variant="contained" color="primary">New project</Button>
                            </FormControl>
                            <FormControl className={classes.formControl}>
                                <Select
                                    labelId="projet-select-label"
                                    value={selectedProject}
                                    onChange={(e) => setSelectedProject(e.target.value)}
                                    >
                                    <MenuItem value={-1}>
                                        <em>Projects</em>
                                    </MenuItem>
                                    {projects.map((element, i) => <MenuItem key={element.name} value={i}>{element.name  }</MenuItem>)}
                                </Select>
                            </FormControl>
                        </FormGroup>
                        {selectedProject !== -1 && <ProjectEditor projectData={projects[selectedProject]}/>}
                        
                    </form>
                </Container>
            </main>
            <div className={classes.appBarSpacer}/>
            <Footer/>
        </div>
    );
}