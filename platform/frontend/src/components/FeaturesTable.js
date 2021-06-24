import React, {forwardRef} from "react";
import MaterialTable from "material-table";
import AddBox from '@material-ui/icons/AddBox';
import ArrowDownward from '@material-ui/icons/ArrowDownward';
import Check from '@material-ui/icons/Check';
import ChevronLeft from '@material-ui/icons/ChevronLeft';
import ChevronRight from '@material-ui/icons/ChevronRight';
import Clear from '@material-ui/icons/Clear';
import DeleteOutline from '@material-ui/icons/DeleteOutline';
import Edit from '@material-ui/icons/Edit';
import FilterList from '@material-ui/icons/FilterList';
import FirstPage from '@material-ui/icons/FirstPage';
import LastPage from '@material-ui/icons/LastPage';
import Remove from '@material-ui/icons/Remove';
import SaveAlt from '@material-ui/icons/SaveAlt';
import Search from '@material-ui/icons/Search';
import ViewColumn from '@material-ui/icons/ViewColumn';
import {putContent} from "../services/content.service"

const tableIcons = {
    Add: forwardRef((props, ref) => <AddBox {...props} ref={ref}/>),
    Check: forwardRef((props, ref) => <Check {...props} ref={ref}/>),
    Clear: forwardRef((props, ref) => <Clear {...props} ref={ref}/>),
    Delete: forwardRef((props, ref) => <DeleteOutline {...props} ref={ref}/>),
    DetailPanel: forwardRef((props, ref) => <ChevronRight {...props} ref={ref}/>),
    Edit: forwardRef((props, ref) => <Edit {...props} ref={ref}/>),
    Export: forwardRef((props, ref) => <SaveAlt {...props} ref={ref}/>),
    Filter: forwardRef((props, ref) => <FilterList {...props} ref={ref}/>),
    FirstPage: forwardRef((props, ref) => <FirstPage {...props} ref={ref}/>),
    LastPage: forwardRef((props, ref) => <LastPage {...props} ref={ref}/>),
    NextPage: forwardRef((props, ref) => <ChevronRight {...props} ref={ref}/>),
    PreviousPage: forwardRef((props, ref) => <ChevronLeft {...props} ref={ref}/>),
    ResetSearch: forwardRef((props, ref) => <Clear {...props} ref={ref}/>),
    Search: forwardRef((props, ref) => <Search {...props} ref={ref}/>),
    SortArrow: forwardRef((props, ref) => <ArrowDownward {...props} ref={ref}/>),
    ThirdStateCheck: forwardRef((props, ref) => <Remove {...props} ref={ref}/>),
    ViewColumn: forwardRef((props, ref) => <ViewColumn {...props} ref={ref}/>)
};

const FEATURE_NAMES = ['T', 'D']

const parseFeatures = (data) => {
    return []
}


export default function FeaturesTable(props) {


    const [columns] = React.useState([
        {
            title: 'information Extraite', field: 'span',
            editComponent: props => (
                <input
                    type="text"
                    value={props.value}
                    onChange={e => props.onChange(e.target.value)}
                />
            )
        },
        {title: 'précision en(%)', field: 'acc', type: 'numeric'},
        {
            title: "label",
            field: "label",
            lookup: FEATURE_NAMES.reduce((obj, x) => {
                obj[x] = x;
                return obj;
            }, {}),
          },
    ]);


    return (
        <MaterialTable
            options={{selection: true}}
            title="Résultat Modéle"
            icons={tableIcons}
            columns={columns}
            data={parseFeatures(props.data)}
            editable={{
                onRowAdd: newData =>
                    new Promise((resolve, reject) => {
                        setTimeout(() => {
                            var newFeatures = props.features
                            const user = JSON.parse(localStorage.getItem("currentUser"))
                            if (!newFeatures)
                                newFeatures = {}
                            if (!(newData.label in newFeatures))
                                newFeatures[newData.label] = {}
                            if (!(user.username in newFeatures[newData.label]))
                                newFeatures[newData.label][user.username] = []
                            newFeatures[newData.label][user.username].push({span:(0,0), acc:newData.acc})
                            putContent('/exam-reports/' + props.examId, {features:newFeatures}, resolve)
                        }, 1000);
                    }),
            }}
            parentChildData={(row, rows) => rows.find(a => a.id === row.parentId)}

        />
    )
}
