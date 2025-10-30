package com.example.miniproject7

import android.os.Bundle
import android.widget.TextView
import android.widget.Toast
import com.google.android.material.floatingactionbutton.FloatingActionButton
import androidx.appcompat.app.AppCompatActivity

class CarbonMetricsActivity : AppCompatActivity() {
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_carbon_metrics)

        val username = findViewById<TextView>(R.id.username)
        val accountAge = findViewById<TextView>(R.id.accountAge)
        val refreshButton = findViewById<FloatingActionButton>(R.id.refreshButton)

        // Get each metric card view
        val postsCard = findViewById<android.view.View>(R.id.posts_card)
        val commentsCard = findViewById<android.view.View>(R.id.comments_card)
        val upvotesCard = findViewById<android.view.View>(R.id.upvotes_card)
        val downvotesCard = findViewById<android.view.View>(R.id.downvotes_card)
        val mediaCard = findViewById<android.view.View>(R.id.media_card)
        val carbonCard = findViewById<android.view.View>(R.id.carbon_card)

        // Assign values
        username.text = "TooGlamToGiveADamn_"
        accountAge.text = "Account Age: 3 days"

        postsCard.findViewById<TextView>(R.id.metric_title).text = "Posts"
        postsCard.findViewById<TextView>(R.id.metric_value).text = "2"

        commentsCard.findViewById<TextView>(R.id.metric_title).text = "Comments"
        commentsCard.findViewById<TextView>(R.id.metric_value).text = "4"

        upvotesCard.findViewById<TextView>(R.id.metric_title).text = "Upvotes"
        upvotesCard.findViewById<TextView>(R.id.metric_value).text = "6"

        downvotesCard.findViewById<TextView>(R.id.metric_title).text = "Downvotes"
        downvotesCard.findViewById<TextView>(R.id.metric_value).text = "0"

        mediaCard.findViewById<TextView>(R.id.metric_title).text = "Media Posts"
        mediaCard.findViewById<TextView>(R.id.metric_value).text = "3"

        carbonCard.findViewById<TextView>(R.id.metric_title).text = "Carbon Footprint"
        carbonCard.findViewById<TextView>(R.id.metric_value).text = "0.348 gCO₂e"

        refreshButton.setOnClickListener {
            Toast.makeText(this, "Refreshing metrics...", Toast.LENGTH_SHORT).show()
        }
    }
}
