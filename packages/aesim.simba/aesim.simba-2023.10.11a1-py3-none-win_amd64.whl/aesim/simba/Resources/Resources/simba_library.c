#include "simba_library.h" 
#include <stdlib.h>

/*
 * Type: model_data 
 * --------------------
 * 	Define in the model_data structure the variables required by your model
 */
typedef struct{
    // Insert model variables here.
} model_data;


/*
 * Variable: data 
 * --------------------
 *	Actual model data.
 */
model_data data; 

/*
 * Function: initialize
 * ----------------------------
 *	Called once at the beginning of the simulation. 
 *	All the variables used in the model must be initialized.
 *
 */
void initialize() {
}

/*
 * Function: calculate_outputs
 * ----------------------------
 *	Called once at each time step to calculate model outputs. 
 *
 *	outputs: array of outputs to be calculated. Array size is equal to the number of outputs. 
 *	inputs: array of inputs values. Array size is equal to the number of inputs. 
 *	time: current simulation time 
 *	time_step: current simulation time-step
 *	
 *	Notes:
 *		- A crash may occur if input/outputs arrays are accessed out of bounds.
 *		- In the case of zero-crossing interpolation (switching), a time-step is added at the zero-crossing time (even using the fixed-time step solver).
 */
void calculate_outputs(double* outputs, double* inputs, double time, double time_step) {
}

/*
 * Function: terminate
 * ----------------------------
 *	Called once at the end of the simulation. 
 *	The resources allocated in the initialize function must be released here.
 *
 */
void terminate() {
}

/*
 * Function: snapshot (DO NOT MODIFY)
 * ----------------------------
 *	With the predictive time-step solver, the simulation time does not elapses linearly.
 *	The C Code model needs to support time-travel and a snapshot mechanism is implemented. 
 *	The predictive time-step solver uses it to restore a model to a previous state when needed. 
 *	
 *	 Notes:
 *		- If you think you need to modify this function, think again and don't modify it. 
 *		- If you think you really need to modify this function and SIMBA crashes, contact us and we will be pleased to help.
 */
void* snapshot(snapshot_mode mode, void* snapshot_ptr) {
	model_data* model_data_ptr;
	switch (mode) {
		case SNAPSHOT_CREATE: // Create and return a snapshot of the current model state
			model_data_ptr = (model_data*)malloc(sizeof(model_data));
			if (model_data_ptr == 0) return 0;
			*model_data_ptr = data;
			return (void*)model_data_ptr;

		case SNAPSHOT_UPDATE:  // Update existing snapshot with current model data
			model_data_ptr = (model_data*)snapshot_ptr;
			*model_data_ptr = data;
			return snapshot_ptr;

		case SNAPSHOT_LOAD:  // Restore model data 
			model_data_ptr = (model_data*)snapshot_ptr;
			data = *model_data_ptr;
			return snapshot_ptr;

		case SNAPSHOT_DELETE: // Free the resources allocated in SNAPSHOT_CREATE
			free(snapshot_ptr);
			return 0;
	}
}