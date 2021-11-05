const { Badge, Icon, Popper } = MaterialUI;

class NotificationsButton extends ConnectedComponent {
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
        const { getUrl, postUrl } = this.props;

        const open = Boolean(this.state.anchorEl);
        const id = open ? 'notifications-popper' : undefined;

        const notifications = <NotificationList getUrl={ getUrl } postUrl={ postUrl } eventsHandler={this} />;
        
        const button = (
            <div>
                <Badge badgeContent={this.state.elementCount} aria-describedby={id} color="secondary" onClick={this.onClick} style={{ cursor: 'pointer' }}>
                    <Icon style={{color: 'white'}}>notifications</Icon>
                </Badge>

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