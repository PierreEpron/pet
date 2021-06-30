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

const PREVIEW_MAX_LENGTH = 35

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

export default React.memo(function FeaturesTable(props) {

    const { text, features, onHighlight, onAddFeature } = props;

    // TODO : Refactorize
    const parseFeatures = (data) => {
        var c = 0
        const parsed = []
    
        const feature_names = Object.keys(data)
    
        feature_names.forEach((element) => { 
            parsed.push({id:c, label:element.capitalize()})
            c++;
        })
    
        for(var fkey in data) {
            for (var mkey in data[fkey]){
                const model = data[fkey][mkey]
                parsed.push({id:c, label:mkey, parentId:feature_names.indexOf(fkey)})
                const parendId = c 
                c++;
                for (var vkey in model) {
                    const feature = data[fkey][mkey][vkey]
                    let span = ""
                    if (feature.hasOwnProperty("start") && feature.hasOwnProperty("end")) {
                        span = [feature.start, feature.end]
                    }
                    parsed.push({id:c, label:feature.label, span:span, parentId:parendId})
                    c++;
                }
            }  
        }

        return parsed
    }   

    const handleMouseEnter = (value) => {
        onHighlight(value)
    }
    const handleMouseLeave= () => {
        onHighlight(null)
    }

    const [columns] = React.useState([
        {
            title: 'Label', field: 'label',
        },
        {
            title: "Span",
            field: "span",
            render: (rowData) => {
                if (!rowData.hasOwnProperty("span") || rowData.span === '')
                    return (<span></span>)

                const start = rowData.span[0]
                const end = rowData.span[1]

                let preview = ''
                if (end - start > PREVIEW_MAX_LENGTH)
                    preview = text.substring(start, start + PREVIEW_MAX_LENGTH) + " [...]"
                else 
                    preview = text.substring(start, end)
                return (
                    <span onMouseEnter={()=>handleMouseEnter([start, end])}
                          onMouseLeave={()=>handleMouseLeave(null)}>({start}, {end}) "{preview}"`</span>
                ) }   
          },
    ]);

    return (
        <div>
            <MaterialTable
                options={{selection: true}}
                title="Résultats"
                icons={tableIcons}
                columns={columns}
                data={parseFeatures(features)}
                actions={[
                    {
                    icon: 'add',
                    tooltip: 'Add Feature',
                    isFreeAction: true,
                    onClick: () => onAddFeature(true)
                    }
                ]}
                parentChildData={(row, rows) => rows.find(a => a.id === row.parentId)}
            />
        </div>
    )
})
