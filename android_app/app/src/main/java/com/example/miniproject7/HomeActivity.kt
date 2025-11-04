package com.example.miniproject7

import android.content.Intent
import android.os.Bundle
import android.view.MotionEvent
import android.widget.TextView
import androidx.appcompat.app.AppCompatActivity

class HomeActivity : AppCompatActivity() {
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_home)

        val tv = findViewById<TextView>(R.id.tvWelcome)
        val name = intent.getStringExtra("userName")
        tv.text = "Welcome, ${name ?: "User"}!"
    }

    // Detect touch anywhere on the screen
    override fun onTouchEvent(event: MotionEvent?): Boolean {
        if (event?.action == MotionEvent.ACTION_DOWN) {
            val intent = Intent(this, CarbonMetricsActivity::class.java)
            startActivity(intent)
            return true
        }
        return super.onTouchEvent(event)
    }
}
