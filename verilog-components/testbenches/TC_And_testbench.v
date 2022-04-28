`timescale 10ns / 1ns

module TC_And_testbench ();
    // clock and reset signals
//    reg clk;
//    reg rst;

    // dut (Design Under Test) io
    reg a;
    reg b;
    wire out;
    
    // dut instantiation
    TC_And dut (.in0(a), .in1(b), .out(out));

    // generate clock
//    initial begin
//        clk = 1'b0;
//        forever #1 clk = ~clk;
//    end

    // generate reset
//    initial begin
//        rst = 1'b1;
//        #10
//        rst = 1'b0;
//    end

    // run tests
    initial begin
        // monitor io
        $monitor("time=%3d, a=%b, b=%b, out=%2b\n",
                    $time, a, b, out);
        
        // generate all input combinations with 200ns delays
        {a, b} = 2'b00;
        #20
        {a, b} = 2'b01;
        #20
        {a, b} = 2'b10;
        #20
        {a, b} = 2'b11;
    end
endmodule

