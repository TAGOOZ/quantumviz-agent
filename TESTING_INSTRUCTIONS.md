# Testing Instructions for QuantumViz Agent

## Quick Start Testing (5 minutes)

**Live Demo**: https://quantumviz-agent.netlify.app
**API Backend**: https://quantumviz-agent.onrender.com

## 1. Basic Functionality Tests

**Test 1: Circuit Builder Interface**
1. Open the live demo URL
2. Verify the quantum circuit builder loads with ASCII logo
3. Check that all 8 quantum gates are clickable (H, X, Y, Z, CNOT, CZ, SWAP, T)
4. Confirm qubit selection dropdowns work (0-3)

**Test 2: Sample Circuits**
1. Click "Bell State (Entanglement)" button
2. Verify circuit display shows: H gate on qubit 0, CNOT on qubits 0→1
3. Try other samples: "Superposition", "GHZ State", "Quantum Teleportation"
4. Confirm each loads different gate combinations

**Test 3: Manual Gate Addition**
1. Select "Qubit 0" from dropdown
2. Click "H" gate button
3. Verify circuit display updates with Hadamard gate
4. Add CNOT gate with target qubit 1
5. Check circuit shows both gates in sequence

## 2. Quantum Simulation Tests

**Test 4: Bell State Simulation**
1. Load "Bell State" sample circuit
2. Click "RUN SIMULATION" button
3. Expected results:
   - |00⟩: ~50% probability (~512 shots)
   - |11⟩: ~50% probability (~512 shots)
   - No |01⟩ or |10⟩ states (entanglement proof)
4. Verify 3D bar chart visualization appears
5. Check statistics panel shows: 2 gates, 2 qubits, depth 2

**Test 5: Superposition Test**
1. Load "Superposition" sample
2. Run simulation
3. Expected: Equal probability for |0⟩ and |1⟩ states
4. Verify visualization shows balanced distribution

## 3. Advanced Features Tests

**Test 6: Keyboard Shortcuts**
1. Press 'H' key → should add Hadamard gate
2. Press 'X' key → should add Pauli-X gate
3. Press 'C' key → should add CNOT gate
4. Press 'R' key → should run simulation
5. Press 'U' key → should undo last gate
6. Press 'Esc' key → should reset circuit

**Test 7: Undo/Reset Functionality**
1. Add several gates manually
2. Click "Undo" button → last gate should disappear
3. Click "Reset" button → entire circuit should clear
4. Verify circuit display shows "No gates added"

**Test 8: Export Feature**
1. Create any circuit with 2-3 gates
2. Click "Export" button
3. Verify file downloads with circuit text
4. Check file contains readable quantum circuit description

## 4. AI and Cloud Features Tests

**Test 9: AI Explanation (if AWS configured)**
1. Create Bell State circuit
2. Click "AI Explain" button
3. Expected: Detailed explanation of entanglement
4. Should mention quantum concepts, measurement probabilities
5. If AWS unavailable: fallback explanation should appear

**Test 10: Backend Health Check**
1. Check "Backend Status" indicator in results panel
2. Should show "Connected" in green if backend is healthy
3. Test API directly: `curl https://quantumviz-agent.onrender.com/api/health`
4. Expected JSON response with status: "healthy"

## 5. Error Handling Tests

**Test 11: Invalid Circuit Operations**
1. Try adding CNOT gate without setting target qubit
2. Verify error message appears
3. Try running simulation on empty circuit
4. Should show "No gates in circuit" error

**Test 12: Network Resilience**
1. Disconnect internet briefly
2. Try running simulation
3. Should show appropriate error message
4. Reconnect and verify functionality resumes

## 6. Performance Tests

**Test 13: Complex Circuit Performance**
1. Create GHZ state (3-qubit entanglement)
2. Run simulation multiple times
3. Verify results are consistent
4. Check simulation completes within 5 seconds

**Test 14: Rapid Gate Addition**
1. Quickly add 10+ gates using keyboard shortcuts
2. Verify all gates register correctly
3. Check undo functionality works for all gates

## 7. Cross-Browser Compatibility

**Test 15: Browser Testing**
- Chrome: Full functionality expected
- Firefox: Verify Plotly visualizations work
- Safari: Check WebGL support for 3D graphics
- Mobile browsers: Responsive design test

## 8. API Endpoint Testing

**Test 16: Direct API Testing**
```bash
# Health check
curl https://quantumviz-agent.onrender.com/api/health

# Add gate
curl -X POST https://quantumviz-agent.onrender.com/api/add_gate \
  -H "Content-Type: application/json" \
  -d '{"gate_type": "H", "qubit": 0}'

# Run simulation
curl -X POST https://quantumviz-agent.onrender.com/api/simulate

# Reset circuit
curl -X POST https://quantumviz-agent.onrender.com/api/reset
```

## 9. Expected Results Reference

**Bell State Results**:
- States: |00⟩ and |11⟩ only
- Probabilities: ~50% each
- Total shots: 1024

**Superposition Results**:
- States: |0⟩ and |1⟩
- Probabilities: ~50% each

**GHZ State Results**:
- States: |000⟩ and |111⟩ only
- Probabilities: ~50% each
- Demonstrates 3-qubit entanglement

## 10. Troubleshooting Common Issues

**Issue**: Backend shows "Offline"
- **Solution**: Wait 30 seconds for Render cold start

**Issue**: Visualization doesn't appear
- **Solution**: Check browser console, ensure Plotly.js loads

**Issue**: Gates don't add
- **Solution**: Verify target qubit selection for 2-qubit gates

**Issue**: Simulation fails
- **Solution**: Ensure at least one gate is in circuit

## Success Criteria

✅ All sample circuits load and simulate correctly
✅ Manual gate addition works with visual feedback
✅ Quantum simulation produces expected probability distributions
✅ 3D visualizations render properly
✅ Keyboard shortcuts respond correctly
✅ Error handling provides clear feedback
✅ Backend API responds within 5 seconds
✅ Cross-browser compatibility maintained

## Demo Script for Judges (2 minutes)

1. **Load Bell State** (15 seconds)
   - Click "Bell State" sample
   - Show entangled circuit in display

2. **Run Simulation** (30 seconds)
   - Click "RUN SIMULATION"
   - Point out 50/50 |00⟩ and |11⟩ distribution
   - Highlight 3D visualization

3. **Try AI Explanation** (30 seconds)
   - Click "AI Explain"
   - Show intelligent quantum concept explanation

4. **Interactive Demo** (45 seconds)
   - Use keyboard shortcuts (H, C, R)
   - Show real-time circuit building
   - Demonstrate undo/reset functionality

**Key Message**: "This is quantum computing made accessible through AI-powered visualization - no PhD required!"

---

**Testing Complete!** The application demonstrates quantum circuit building, simulation, and AI-powered education in an intuitive web interface.