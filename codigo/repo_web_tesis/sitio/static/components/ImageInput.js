
class ImageInput extends React.Component {
    constructor(props) {
        super(props);

        this.id = _.uniqueId('file-image-field');

        this.state = {
            placeholder: false,
            src: props.src || null
        }

        this.handleClick = this.handleClick.bind(this);
        this.showPlaceholder = this.showPlaceholder.bind(this);
        this.hidePlaceholder = this.hidePlaceholder.bind(this);
        this.displayPreview = this.displayPreview.bind(this);
    }

    handleClick() {
        if (!this.props.readonly) {
            const selector = '#' + this.id + " input[type='file']";
            const input = document.querySelector(selector);

            if (input) {
                input.click();
            }
        }
    }

    showPlaceholder() {
        this.setState((prev) => ({
            placeholder: true
        }))
    }

    hidePlaceholder() {
        this.setState((prev) => ({
            placeholder: false
        }))
    }

    setSrc(value) {
        this.setState((prev) => ({
            src: value
        }))
    }

    displayPreview() {
        const imageInput = document.querySelector(`#${this.id} input[type='file']`);

        if (imageInput) {
            const [image] = imageInput.files;

            if (image) {
                this.setSrc(URL.createObjectURL(image));
                document.dispatchEvent(new Event(`ImageInput[${this.id}]:changed`));
            }
        }
    }

    getPlaceHolder() {
        if (this.state.placeholder && !this.props.readonly) {
            return this.props.placeholderLoad;
        } else if (!this.state.src) {
            return this.props.placeholderShow;
        } else {
            return this.state.src;
        }
    }

    render() {
        const { readonly, avatarProps, name } = this.props;

        const input = !readonly
            ? (<input name={name || 'imagen'} accept="image/*" onChange={this.displayPreview} style={{ display: 'none' }} type="file"></input>)
            : null;

        return (
            <MaterialUI.Box id={this.id}>
                <MaterialUI.Avatar variant={this.props.variant || null} style={{ height: this.props.height || 124, width: this.props.width || 124, cursor: !readonly ? 'pointer' : 'default' }} {...(avatarProps || {})} src={this.getPlaceHolder()} onClick={this.handleClick} onMouseEnter={this.showPlaceholder} onMouseLeave={this.hidePlaceholder}></MaterialUI.Avatar>
                {input}
            </MaterialUI.Box>
        )
    }
}
