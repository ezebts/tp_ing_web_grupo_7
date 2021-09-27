const { OutlinedInput } = MaterialUI;
const { InputLabel } = MaterialUI;
const { MenuItem } = MaterialUI;
const { FormControl } = MaterialUI;
const { ListItemText } = MaterialUI;
const { Select } = MaterialUI;
const { Checkbox } = MaterialUI;

const ITEM_HEIGHT = 48;
const ITEM_PADDING_TOP = 8;
const MenuProps = {
    PaperProps: {
        style: {
            maxHeight: ITEM_HEIGHT * 4.5 + ITEM_PADDING_TOP,
            width: 250,
        },
    },
};

function MultiSelectInput(props) {
    const id = _.uniqueId('multi-select-field');

    const [objName, setObjName] = React.useState(props.value || []);

    const handleChange = (event) => {
        const {
            target: { value },
        } = event;
        setObjName(
            // On autofill we get a the stringified value.
            typeof value === 'string' ? value.split(',') : value,
        );
    };

    return (
        <div>
            <FormControl className={props.className || ''}>
                <InputLabel id={id + "-label"} styles={{ margin: '5px' }}>{props.label}</InputLabel>
                <Select
                    placeholder={props.placeholder}
                    name={props.name}
                    labelId={id + "-label"}
                    id={id}
                    multiple
                    value={objName}
                    onChange={handleChange}
                    input={<OutlinedInput label="Tag" />}
                    renderValue={(selected) => selected ? selected.join(', ') : (props.placeholder || '')}
                    MenuProps={MenuProps}
                >
                    {(props.options || []).map((obj) => (
                        <MenuItem key={obj.name} value={obj.name}>
                            <Checkbox checked={objName.indexOf(obj.name) > -1} />
                            <ListItemText primary={obj.name} />
                        </MenuItem>
                    ))}
                </Select>
            </FormControl>
        </div>
    );
}