var Calendar = React.createClass({
    componentDidMount() {
        var component = Object(this);
        getAllEvents(function(events) {
            events.sort(component.sortEvent);
            component.setState({
                event_items: events
            });
        });
    },
    getInitialState: function() {
        return {
            event_items: []
        };
    },
    render: function() {
        if (this.state.event_items.length) {
            var display_items = this.state.event_items.map( function (display, i) {
                if (!display.cancelled) {
                    display.cancelled = false;
                }
                return (
                    <Event id = {i} info = {display} cancelled = {display.cancelled} />
                );
            });
            return (
                <div className = "calendar">{ display_items }</div>
            );
        } else {
            return null;
        }
    },
    sortEvent: function(a, b) {
        if (a.year < b.year) {
            return -1;
        }
        if (a.year > b.year) {
            return 1
        }
        if (a.month < b.month) {
            return -1;
        }
        if (a.month > b.month) {
            return 1;
        }
        if (a.day < b.day) {
            return -1;
        }
        if (a.day > b.day) {
            return -1;
        }
        return 0;
    }
});

var Event = React.createClass({
    render: function() {
        var style = "event" + (this.props.cancelled ? " cancelled" : "") ;
        return (
            <div className = {style} key = {this.props.id}>
                <div className = "event-name">{this.props.info.occasion}
                {this.props.cancelled && " ( Event Cancelled )"}</div> 
                <div className = "event-time">{this.props.info.month}/
                {this.props.info.day}/{this.props.info.year}</div>
                <div className = "event-invited">{this.props.info.invited_count} people invited</div>
            </div>
        );
        //{this.props.month}, {this.props.day}, {this.props.year}
    }
});

ReactDOM.render(
    <Calendar />,
    document.getElementById("calendar")
);