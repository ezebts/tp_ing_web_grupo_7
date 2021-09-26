const withStyles = MaterialUI.withStyles;

const Card = MaterialUI.Card;
const CardHeader = MaterialUI.CardHeader;
const CardMedia = MaterialUI.CardMedia;
const CardContent = MaterialUI.CardContent;
const CardActions = MaterialUI.CardActions;
const CardActionArea = MaterialUI.CardActionArea;
const Link = MaterialUI.Link;
const Collapse = MaterialUI.Collapse;
const Avatar = MaterialUI.Avatar;
const IconButton = MaterialUI.IconButton;
const Typography = MaterialUI.Typography;
const Icon = MaterialUI.Icon;

const red = MaterialUI.colors.red;
const grey = MaterialUI.colors.grey;

class PublicacionCard extends React.Component {
    static useStyles = (theme) => ({
        root: {

        },
        media: {
            height: 0,
            paddingTop: '56.25%', // 16:9
        },
        avatar: {
            backgroundColor: red[500],
            float: 'left',
            border: '2px solid white',
        },
        avatarPlus: {
            backgroundColor: grey[500],
            float: 'left',
            border: '2px solid white',
        }
    });

    constructor(props) {
        super(props);

        this.state = {
        }
    }

    render() {
        const { classes, autores, titulo, fecha, resumen, resumenTitle, ver, imagen } = this.props;

        const autoresAvatars = [];

        let key = 0;
        for (const autor of (autores || [])) {
            const splitted = autor.fields.full_name.split(' ');

            const first = splitted[0].toUpperCase()[0];
            const last = splitted[splitted.length - 1].toUpperCase()[0];
            const style = { zIndex: (autores.length - key) + 1 };

            if (key > 0) {
                style.marginLeft = '-12px';
            }

            autoresAvatars.push(
                <Avatar src={autor.image} style={style} key={key} aria-label={autor.name} alt={autor.name} className={classes.avatar}>
                    {!autor.image ? `${first}${last}` : null}
                </Avatar>
            )

            key++;
        }

        let parsedAvatars = [];

        if (autoresAvatars.length > 2) {
            parsedAvatars.push(autoresAvatars[0]);
            parsedAvatars.push(autoresAvatars[1]);

            parsedAvatars.push(
                <Avatar style={{ zIndex: 1, marginLeft: '-12px' }} key={key + 1} aria-label='autores' alt='autores' className={classes.avatarPlus}>
                    {`+${autoresAvatars.length - 2}`}
                </Avatar>
            );
        }
        else {
            parsedAvatars = autoresAvatars;
        }

        return (
            <Card className={classes.root}>
                {
                    autores || titulo ?
                        <CardHeader
                            avatar={
                                <div>
                                    {parsedAvatars}
                                </div>
                            }
                            action={
                                autores ?
                                    <IconButton aria-label="settings">
                                        <Icon>more_vert</Icon>
                                    </IconButton> : null
                            }
                            {...(titulo ? { title: titulo } : {})}
                            subheader={fecha}
                        /> : null
                }
                <CardActionArea component={Link} href={ver}>
                    {
                        imagen ?
                            (<CardMedia
                                className={classes.media}
                                image={imagen}
                                title={titulo}
                            />) : null
                    }
                    <CardContent>
                        <Typography variant="body1" color="textSecondary" component="p">
                            {resumenTitle}
                        </Typography>
                        <Typography variant="body1" color="textSecondary" component="p">
                            {resumen}
                        </Typography>
                    </CardContent>
                </CardActionArea>
                {
                    autores ?
                        (<CardActions disableSpacing>
                            <IconButton aria-label="like">
                                <Icon className="material-icons-outlined">thumb_up</Icon>
                            </IconButton>
                            <IconButton aria-label="share">
                                <Icon>share</Icon>
                            </IconButton>
                        </CardActions>) : null
                }
            </Card>
        );
    }
}

PublicacionCard = withStyles(PublicacionCard.useStyles)(PublicacionCard);
