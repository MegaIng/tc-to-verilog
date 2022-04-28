`timescale 10ns / 1ns

module TC_Counter_testbench ();
    // clock and reset signals
    reg clk;
    reg rst;

    // dut (Design Under Test) io
    reg save;
    reg [7:0] in;
    wire [7:0] out;
    
    // dut instantiation
    TC_Counter dut (.clk(clk), .rst(rst), .save(save), .in(in), .out(out));

    // generate clock
    initial begin
        clk = 1'b0;
        forever #1 clk = ~clk;
    end

    // generate reset
    initial begin
        rst = 1'b1;
        #10
        rst = 1'b0;
    end

    // run tests
    initial begin
        // monitor io
        $monitor("time=%3d, save=%b, in=%b, out=%b\n",
                    $time, save, in, out);
        
        // generate all input combinations with 200ns delays
        save = 1'b0;
        in = 8'b0000_0000;
        #20
        save = 1'b1;
        #20
        save = 1'b0;
        #20
        in = 8'b1000_0000;
        save = 1'b1;
        #20
        save = 1'b0;
    end
endmodule

