import { patch } from "@web/core/utils/patch";
import { ProjectTaskStateSelection } from "@project/components/project_task_state_selection/project_task_state_selection";
patch(ProjectTaskStateSelection.prototype, {
	setup() {
        super.setup();
        this.icons["05_return_sav"] = "fa fa-lg fa-undo";
        this.colorIcons['05_return_sav'] = "text-primary";
        this.colorButton['05_return_sav'] = "btn-outline-primary";

    },
	get options() {
		const options = super.options;
		options.push(['05_return_sav', 'Return SAV'])
		return options
	},

});