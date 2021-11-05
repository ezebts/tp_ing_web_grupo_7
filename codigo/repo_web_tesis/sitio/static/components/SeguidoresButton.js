const { Button, Icon, Popper } = MaterialUI;

class SeguidoresButton extends ConnectedComponent {
    constructor(props) {
        super(props);
        
        this.onClick = this.onClick.bind(this);

        this.state = {
            anchorEl: null,
            hasElements: false,
            elementCount: 0
        };
    }

    setAnchorEl(value) {
        this.setState(prev => ({ anchorEl: value }));
    }

    onClick(event) {
        this.setAnchorEl(this.state.anchorEl ? null : event.currentTarget);
    }

    hasElements(count) {
        this.setState(prev => ({
            hasElements: true,
            elementCount: count
        }))
    }

    updateState(prev, parsed) {
        if (parsed && parsed.length) {
            this.hasElements(parsed.length);
        } else {
            this.hasntElements();
        }

        return parsed;
    }

    hasntElements() {
        this.setState(prev => ({
            hasElements: false,
            elementCount: 0
        }))
    }

    render() {
        const { getUrl, postUrl, seguidores } = this.props;

        const open = Boolean(this.state.anchorEl);
        const id = open ? 'notifications-popper' : undefined;

        const notifications = <SeguidoresList getUrl={ getUrl } postUrl={ postUrl } seguidores={seguidores} eventsHandler={this} />;
        
        const button = (
            <div style={{float: 'left'}}>
                <Button type="button" aria-describedby={id} color="primary" onClick={this.onClick}>
                    { seguidores ? `Seguidores (${ this.state.elementCount })` : `Seguidos (${ this.state.elementCount })` }
                </Button>

                <Popper 
                placement="bottom"
                id={id}
                open={open}
                anchorEl={this.state.anchorEl}
                style={{zIndex: 9999}}
                >
                    <Box sx={{ border: '1px solid black', p: 0, bgcolor: 'background.paper', zIndex: 9999 }}>
                        { notifications }
                    </Box>
                </Popper>
            </div>
        );

        return button;
    }
}