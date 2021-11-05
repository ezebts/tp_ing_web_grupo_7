const { List, ListItem, ListItemText, Button, Divider, Typography, ListItemAvatar, Avatar } = MaterialUI;

class SeguidoresList extends ConnectedComponent {
    constructor(props) {
        super(props);

        this.state = {
            notifications: []
        }

        this.seguidores = props.seguidores;

        this.eventsHandler = props.eventsHandler || {};
    }

    parseNotification(json) {
        return {
            id: json.pk,
            link: json.fields.perfil_url,
            title: json.fields.username,
            img: json.fields.imagen_url,
            text: this.seguidores ? 'Seguidor' : 'Siguiendo'
        }
    }

    parseJsonResponse(json) {
        const notifications = [];

        for(const notification of (json || [])) {
            notifications.push(this.parseNotification(notification));
        }

        return notifications;
    }

    updateState(prev, parsed) {
        const notifications = parsed || [];

        if (notifications.length) {
            if (this.eventsHandler && this.eventsHandler.hasElements) {
                this.eventsHandler.hasElements(notifications.length);
            }
        } else {
            if (this.eventsHandler && this.eventsHandler.hasntElements) {
                this.eventsHandler.hasntElements();
            }
        }

        return { notifications };
    }

    focusNewData() { }

    render() {
        const notifications = [];
        
        let key = 1;

        for(const notification of this.state.notifications) {
            const divider = (<Divider variant="inset" style={{ listStyle: 'none' }} component="li" />);

            const title = (
            <React.Fragment>
                <Typography
                sx={{ display: 'inline' }}
                component="span"
                variant="caption"
                style={{fontWeight: 'bold'}}
                >
                    { notification.title }
                </Typography>
            </React.Fragment>
            );

            const text = (
            <React.Fragment>
                <Typography
                sx={{ display: 'inline' }}
                component="span"
                variant="caption"
                style={{fontWeight: !notification.title ? 'bold' : 'regular'}}
                >
                    { notification.text }
                </Typography>
            </React.Fragment>
            );

            const notificationComponent = (
                <ListItem key={key} alignItems="flex-start" component={Button} href={ notification.link }>
                    <ListItemText inset primary={ title } secondary={ text } />
                    <ListItemAvatar>
                        <Avatar alt={ notification.title } src={ notification.img } />
                    </ListItemAvatar>
                </ListItem>
            );
            
            if (key > 1) {
                notifications.push(divider);
            }
            
            key++;
            
            notifications.push(notificationComponent);
        }

        return notifications;
    }
}
