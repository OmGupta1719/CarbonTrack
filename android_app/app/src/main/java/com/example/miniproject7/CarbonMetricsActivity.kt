package com.example.miniproject7

import android.os.Bundle
import android.view.View
import android.widget.TextView
import android.widget.Toast
import androidx.appcompat.app.AppCompatActivity
import com.google.android.material.floatingactionbutton.FloatingActionButton
import okhttp3.*
import org.json.JSONObject
import java.io.IOException

class CarbonMetricsActivity : AppCompatActivity() {

    private val client = OkHttpClient()

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_carbon_metrics)

        // Set metric titles (don't change layout)
        findViewById<View>(R.id.posts_card)
            .findViewById<TextView>(R.id.metric_title).text = "Posts"

        findViewById<View>(R.id.comments_card)
            .findViewById<TextView>(R.id.metric_title).text = "Comments"

        findViewById<View>(R.id.upvotes_card)
            .findViewById<TextView>(R.id.metric_title).text = "Upvotes"

        findViewById<View>(R.id.downvotes_card)
            .findViewById<TextView>(R.id.metric_title).text = "Downvotes"

        findViewById<View>(R.id.media_card)
            .findViewById<TextView>(R.id.metric_title).text = "Media Intensity"

        findViewById<View>(R.id.carbon_card)
            .findViewById<TextView>(R.id.metric_title).text = "Carbon Emission"


        // Header views
        val usernameView = findViewById<TextView>(R.id.username)
        val accountAgeView = findViewById<TextView>(R.id.accountAge)
        val carbonSummary = findViewById<TextView>(R.id.carbonSummary)

        // Metric cards: find the root view of include, then the TextView inside
        val postsCard = findViewById<View>(R.id.posts_card).findViewById<TextView>(R.id.metric_value)
        val commentsCard = findViewById<View>(R.id.comments_card).findViewById<TextView>(R.id.metric_value)
        val mediaCard = findViewById<View>(R.id.media_card).findViewById<TextView>(R.id.metric_value)
        val carbonCard = findViewById<View>(R.id.carbon_card).findViewById<TextView>(R.id.metric_value)

        val refreshButton = findViewById<FloatingActionButton>(R.id.refreshButton)

        // Refresh button click
        refreshButton.setOnClickListener {
            Toast.makeText(this, "Fetching latest metrics...", Toast.LENGTH_SHORT).show()
            refreshButton.isEnabled = false
            fetchMetrics(usernameView, accountAgeView, postsCard, commentsCard, mediaCard, carbonCard, carbonSummary) {
                // Re-enable button after fetch
                runOnUiThread { refreshButton.isEnabled = true }
            }
        }
    }

    private fun fetchMetrics(
        usernameView: TextView,
        accountAgeView: TextView,
        postsView: TextView,
        commentsView: TextView,
        mediaView: TextView,
        carbonView: TextView,
        carbonSummary: TextView,
        onComplete: (() -> Unit)? = null
    ) {

//        FOR EMULATOR
        val request = Request.Builder()
            .url("http://10.0.2.2:5000/calculate") // Emulator localhost
            .build()

        //FOR PHONE
//        val request = Request.Builder()
//            .url("http://<IP-ADDRESS>/calculate") // Emulator localhost
//            .build()

        client.newCall(request).enqueue(object : Callback {
            override fun onFailure(call: Call, e: IOException) {
                runOnUiThread {
                    Toast.makeText(this@CarbonMetricsActivity, "Failed to fetch data", Toast.LENGTH_SHORT).show()
                    onComplete?.invoke()
                }
            }

            override fun onResponse(call: Call, response: Response) {
                if (!response.isSuccessful) {
                    runOnUiThread {
                        Toast.makeText(this@CarbonMetricsActivity, "Error: ${response.code}", Toast.LENGTH_SHORT).show()
                        onComplete?.invoke()
                    }
                    return
                }

                response.body?.string()?.let { body ->
                    try {
                        val json = JSONObject(body)
                        val summary = json.getJSONObject("summary")

                        val username = summary.getString("username")
                        val age = summary.getInt("account_age_days")
                        val posts = summary.getInt("total_posts")
                        val comments = summary.getInt("total_comments")
                        val media = summary.getDouble("media_intensity")
                        val carbon = summary.getDouble("total_carbon_gCO2e")

                        runOnUiThread {
                            usernameView.text = username
                            accountAgeView.text = "Account Age: $age days"
                            postsView.text = posts.toString()
                            commentsView.text = comments.toString()
                            mediaView.text = String.format("%.2f", media)
                            carbonView.text = String.format("%.2f gCO₂e", carbon)
                            carbonSummary.text = String.format("%.2f gCO₂e emitted", carbon)
                            onComplete?.invoke()
                        }
                    } catch (e: Exception) {
                        runOnUiThread {
                            Toast.makeText(this@CarbonMetricsActivity, "Invalid response format", Toast.LENGTH_SHORT).show()
                            onComplete?.invoke()
                        }
                    }
                } ?: runOnUiThread { onComplete?.invoke() }
            }
        })
    }
}
