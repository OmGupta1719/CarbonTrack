package com.example.miniproject7

import android.os.Bundle
import android.widget.TextView
import androidx.appcompat.app.AppCompatActivity

class CarbonMetricsActivity : AppCompatActivity() {

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_carbon_metrics)

        val tvTotalCarbon: TextView = findViewById(R.id.tvTotalCarbon)
        val tvPosts: TextView = findViewById(R.id.tvPosts)
        val tvComments: TextView = findViewById(R.id.tvComments)
        val tvMediaIntensity: TextView = findViewById(R.id.tvMediaIntensity)
        val tvEngagement: TextView = findViewById(R.id.tvEngagement)

        // Data from Reddit carbon footprint analysis
        val totalCarbon = 0.348  // grams CO₂e
        val totalPosts = 2
        val totalComments = 4
        val mediaIntensity = 0.25
        val totalEngagement = 6 // derived = comments + posts' engagements

        tvTotalCarbon.text = "$totalCarbon gCO₂e"
        tvPosts.text = totalPosts.toString()
        tvComments.text = totalComments.toString()
        tvMediaIntensity.text = mediaIntensity.toString()
        tvEngagement.text = totalEngagement.toString()
    }
}