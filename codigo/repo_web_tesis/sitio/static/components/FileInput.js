
class FileInput extends React.Component {
    constructor(props) {
        super(props);
        this.id = _.uniqueId('file-field');
        this.handleClick = this.handleClick.bind(this);
        this.handleUpload = this.handleUpload.bind(this);

        this.state = {
            fileName: 'No file uploaded yet.'
        };
    }

    setFileName(name) {
        this.setState((prev) => ({
            fileName: name
        }))
    }

    handleUpload() {
        const selector = `#${this.id} input[type='file']`;
        const fullPath = document.querySelector(selector).value;

        if (fullPath) {
            const startIndex = (fullPath.indexOf('\\') >= 0 ? fullPath.lastIndexOf('\\') : fullPath.lastIndexOf('/'));
            let filename = fullPath.substring(startIndex);

            if (filename.indexOf('\\') === 0 || filename.indexOf('/') === 0) {
                filename = filename.substring(1);
            }

            this.setFileName(filename);
        }
    }

    handleClick() {
        const selector = `#${this.id} input[type='file']`;
        const input = document.querySelector(selector);

        if (input) {
            input.click();
        }
    }

    render() {
        const { name, accept, required } = this.props;

        return (
            <MaterialUI.Box id={this.id}>
                <MaterialUI.Button onClick={this.handleClick} variant="outlined" startIcon={<MaterialUI.Icon>upload_file</MaterialUI.Icon>}>
                    AGREGAR DOCUMENTO
                    <input type="file" name={name} onChange={this.handleUpload} hidden accept={accept}></input>
                </MaterialUI.Button>
                <span style={{ marginLeft: '10px' }}>{this.state.fileName}</span>
            </MaterialUI.Box >
        )
    }
}
