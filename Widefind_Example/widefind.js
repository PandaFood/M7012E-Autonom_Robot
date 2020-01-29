var rethink = require('rethinkdb')

/*  DB CONFIG  */
const Host = ''
const Port = 
const User = ''
const Pass = ''
/* ----------- */

/**
 * Function to get all posts from DB. Mostly used for debug when sensors are down.
 *
*/
this.GetLatestUpdates = function () {
	
// Standard opening the connection
rethink.connect({ host: Host, port: Port, user: User, password: Pass }, function (error, database) {
  if (error) throw error
  
  // A request to just get all rows from the database, Same as SQL Query: SELECT * FROM table;
  rethink.db('wf100').table('current_state').run(database, function (error, result) {
	if (error) { throw error }

	result.each(function (error, row) {
	  if (error) { throw error }
	  
	  console.log(row)
	})
  })
})
}

/**
 * Function to start fetching Widefind data from database.
 *
*/
this.GetUpdateStream = function () {
rethink.connect({ host: Host, port: Port, user: User, password: Pass }, function (error, database) {
  if (error) { throw error }

  // This function utlizes the 'real-time'-aspect of rethinkDB and opens up a listener which gets a result
  //			as soon as the database gets it.
  rethink.db('wf100').table('current_state').changes().run(database, function (error, result) {
	if (error) { throw error }

	result.each(function (error, row) {
	  if (error) { throw error }

	  console.log(row)
	})
  })
})
}

