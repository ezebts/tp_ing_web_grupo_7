class PasswordField extends React.Component {
    constructor(props) {
        super(props);

        this.state = {
            showPassword: false
        };

        this.togglePassword = this.togglePassword.bind(this);
    }

    togglePassword() {
        this.setState(prevState => ({
            showPassword: !prevState.showPassword
        }))
    }

    render() {
        return (
            <MaterialUI.TextField
                {...this.props.InputProps}
                type={this.state.showPassword ? 'text' : 'password'}
                autoComplete="current-password"
                InputProps={{
                    endAdornment: (
                        <MaterialUI.InputAdornment position="end">
                            <MaterialUI.IconButton
                                onClick={this.togglePassword}
                                aria-label="toggle password visibility"
                            >
                                {
                                    this.state.showPassword
                                        ? <MaterialUI.Icon>visibility</MaterialUI.Icon>
                                        : <MaterialUI.Icon>visibility_off</MaterialUI.Icon>
                                }
                            </MaterialUI.IconButton>
                        </MaterialUI.InputAdornment>
                    )
                }}
                required
            ></MaterialUI.TextField>
        )
    }
}