
class ImageUploadForm extends React.Component {
    constructor(props) {
        super(props);
        this.id = _.uniqueId('upload-image-form');
        this.send = this.send.bind(this);
        this.image = React.createRef();
    }

    componentDidMount() {
        const img = this.image.current;

        if (img) {
            document.addEventListener(`ImageInput[${img.id}]:changed`, this.send);
        }
    }

    send() {
        const selector = '#' + this.id + " form";
        const form = document.querySelector(selector);

        if (form) {
            form.submit();
        }
    }

    render() {
        return (
            <div id={this.id}>
                <form action={this.props.uploadto || ''} method="POST" encType="multipart/form-data">
                    <input type="hidden" name="csrfmiddlewaretoken" value={this.props.csrf} />
                    <input type="hidden" name="next" value={this.props.next} />
                    <ImageInput ref={this.image} {...this.props}></ImageInput>
                </form>
            </div>
        )
    }
}
