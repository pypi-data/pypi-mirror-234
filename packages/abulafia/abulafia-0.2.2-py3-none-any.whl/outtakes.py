# Check if tasks are supposed to output the results
for task in self.sequence:

    if hasattr(task, 'pool'):

        # Get the output DataFrame for each task; assign under 'output_data'
        task.output_data = self.client.get_assignments_df(pool_id=task.pool.id)

        # Check if the output should be written to disk
        try:

            if task.conf['actions'] is not None and 'output' in task.conf['actions']:

                # Write the DataFrame to disk
                task.output_data.to_csv(f'{task.name}_{task.pool.id}.csv')

                msg.good(f'Wrote data for task {task.name} ({task.pool.id}) to disk.')

        except KeyError:

            pass