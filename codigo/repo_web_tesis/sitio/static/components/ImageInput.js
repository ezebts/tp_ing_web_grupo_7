
class ImageInput extends React.Component {
    constructor(props) {
        super(props);

        this.id = _.uniqueId('image-input');

        this.state = {
            placeholder: false
        }

        this.handleClick = this.handleClick.bind(this);
        this.showPlaceholder = this.showPlaceholder.bind(this);
        this.hidePlaceholder = this.hidePlaceholder.bind(this);
        this.send = this.send.bind(this);
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

    getPlaceHolder() {
        if (this.state.placeholder && !this.props.readonly) {
            return this.props.placeholderLoad;
        } else if (!this.props.src) {
            return this.props.placeholderShow;
        } else {
            return this.props.src;
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
        const { readonly, avatarProps } = this.props;

        const input = !readonly
            ? (
                <form action={this.props.uploadto || ''} method="POST" encType="multipart/form-data">
                    <input type="hidden" name="csrfmiddlewaretoken" value={this.props.csrf} />
                    <input type="hidden" name="next" value={this.props.next} />
                    <input name="imagen" accept="image/*" onChange={this.send} style={{ display: 'none' }} type="file"></input>
                </form>
            )
            : null;

        return (
            <MaterialUI.Box id={this.id}>
                <MaterialUI.Avatar style={{ height: this.props.height || 124, width: this.props.width || 124, cursor: !readonly ? 'pointer' : 'default' }} {...(avatarProps || {})} src={this.getPlaceHolder()} onClick={this.handleClick} onMouseEnter={this.showPlaceholder} onMouseLeave={this.hidePlaceholder}></MaterialUI.Avatar>
                {input}
            </MaterialUI.Box>
        )
    }
}
