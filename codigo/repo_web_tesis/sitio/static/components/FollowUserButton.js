
class FollowUserButton extends ConnectedComponent {
    constructor(props) {
        super(props);
        this.onClick = this.onClick.bind(this);
        this.state = {
            siguiendo: props.siguiendo
        };
    }

    parseJsonResponse(json) {
        return {
            siguiendo: json != null
        }
    }

    updateState(prev, parsed) {
        return parsed;
    }

    focusNewData() { }

    onClick() {
        this.sendJsonRequest({
            seguir: !this.state.siguiendo
        });

        this.setState((prev) => ({
            siguiendo: !this.state.siguiendo
        }));
    }

    render() {
        return (
            <Button 
            onClick={this.onClick} 
            name="action" 
            role="submit" 
            type="submit" 
            value="SEGUIMIENTO" 
            color="primary"
            variant={ this.state.siguiendo ? "outlined" : "contained" }
            style={{ marginTop: '10px', marginLeft: '2px' }}
            >
               { this.state.siguiendo ? 'DEJAR DE SEGUIR' : 'SEGUIR' }
            </Button>
        )
    }
}
