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
import okhttp3.MediaType.Companion.toMediaType
import okhttp3.RequestBody.Companion.toRequestBody

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
//            .url("http://192.168.53.19:5000/calculate") // Emulator localhost
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

                            // Awareness Views
                            val equivalenceView = findViewById<TextView>(R.id.equivalenceText)
                            val recommendationView = findViewById<TextView>(R.id.recommendationText)
                            val funFactView = findViewById<TextView>(R.id.funFactText)
                            val toolbar = findViewById<androidx.appcompat.widget.Toolbar>(R.id.topAppBar)
                            val progress = findViewById<android.widget.ProgressBar>(R.id.carbonProgress)

                            // --- Calculate dynamic equivalences ---
                            val carKm = carbon / 120.0 // avg car emits 120g CO₂ per km
                            val flightMin = carbon / 90.0 // short flight per min ~90g
                            val treesNeeded = carbon / 21000.0 // 1 tree absorbs 21kg (21000g)

                            val equivalence = String.format(
                                "Your CO₂ = %.1f km of car travel 🚗 or %.2f trees 🌳",
                                carKm, treesNeeded
                            )
                            equivalenceView.text = equivalence

                            // --- Smart Recommendations ---
//                            CHANGE
                            val jsonBody = JSONObject().apply {
                                put("summary", JSONObject().apply {
                                    put("username", "TooGlamToGiveADamn_")
                                    put("account_age_days", 120)
                                    put("total_posts", 35)
                                    put("total_comments", 60)
                                    put("total_video_posts", 8)
                                    put("media_intensity", 0.73)
                                    put("total_carbon_gCO2e", 3.247)
                                })
                            }

                            val mediaType = "application/json; charset=utf-8".toMediaType()
                            val requestBody = jsonBody.toString().toRequestBody(mediaType)


                            val request = Request.Builder()
                                .url("http://10.0.2.2:5000/recommend") // 👈 Use 10.0.2.2 for localhost in Android Emulator
                                .post(requestBody)
                                .build()

                            client.newCall(request).enqueue(object : Callback {
                                override fun onFailure(call: Call, e: IOException) {
                                    runOnUiThread {
                                        recommendationView.text = "Request failed: ${e.message}"
                                    }
                                }

                                override fun onResponse(call: Call, response: Response) {
                                    response.use {
                                        if (!it.isSuccessful) {
                                            runOnUiThread {
                                                recommendationView.text = "Server error: ${it.code}"
                                            }
                                            return
                                        }

                                        val responseText = it.body?.string()
                                        val json = JSONObject(responseText ?: "{}")
                                        val recommendation = json.optString("recommendation", "No recommendation found")

                                        runOnUiThread {
                                            recommendationView.text = recommendation
                                        }

                                    }
                                }
                            })

                            // --- Fun Facts Rotate Randomly ---
                            val funFacts = listOf(
                                "Streaming 1 hour of HD video emits ~36g CO₂ 🎬",
                                "Dark mode can save up to 30% of display energy ⚫",
                                "A single email emits ~4g of CO₂ 📧",
                                "Using Wi-Fi instead of mobile data saves ~20% energy 📶",
                                "Recycling your old phone prevents 55 kg CO₂ waste ♻️"
                            )
                            funFactView.text = funFacts.random()

                            // --- Dynamic Mood Indicator ---
                            val color = when {
                                carbon > 80 -> android.graphics.Color.parseColor("#D32F2F") // Red
                                carbon > 50 -> android.graphics.Color.parseColor("#FFA000") // Orange
                                carbon > 20 -> android.graphics.Color.parseColor("#FBC02D") // Yellow
                                else -> android.graphics.Color.parseColor("#2E7D32") // Green
                            }

                            // Animate smooth transitions
                            val colorAnim = android.animation.ValueAnimator.ofArgb(
                                (toolbar.background as? android.graphics.drawable.ColorDrawable)?.color ?: color,
                                color
                            )
                            colorAnim.duration = 800
                            colorAnim.addUpdateListener { anim ->
                                val c = anim.animatedValue as Int
                                toolbar.setBackgroundColor(c)
                                progress.progressTintList = android.content.res.ColorStateList.valueOf(c)
                            }
                            colorAnim.start()

                            progress.progress = (carbon.coerceAtMost(100.0)).toInt()

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
